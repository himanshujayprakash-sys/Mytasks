import random
import json
import os
import re
from typing import Dict, List, Any
from pathlib import Path
import yaml
import sys
from datetime import datetime

WORK_DIR = Path('.').__str__()
if WORK_DIR not in sys.path:
    sys.path.append(WORK_DIR)

from software.utils.core import OSConnector, DummyOSConnector, connect_os
from software.utils.world_snapshot import restore_into, seed_mode, resolve_seed
from software.utils.time import TimeMachine

CORPUS_PATH = Path(__file__).resolve().parent / "corpus"

# Task world rule, the one server file a task may change. Rows of the allotments base move while the
# lettings round is worked; nothing is posted about any of it, and each change lands before the next
# request to the base, so the reply to the call that sets it off is unchanged. The world file lists
# the changes under _task_source_events: each names the table whose writes set it off and after how
# many records written there (created or updated) it lands, then the fields it sets on existing rows.
# In this world the estates team keys two plot re-measurements into the plot table once the first
# lettings-register line is saved, and a third once eight register lines have been written. A change,
# once it has landed, shows in every session of this world from then on.
# A list page holds as many records as fit in a reply a client keeps whole (about 24,000 characters); the
# offset in the reply picks up where the page stopped.
_PAGE_CHARS = 24000
_TASK_LANDED = set()      # (world dir, event id)
_TASK_WRITES = {}         # (world dir, table name) -> records written there


def _task_scope() -> str:
    return str(Path(os.environ.get("COMPLEXMCP_WORLD_DATA", "")).resolve())


def _to_bool(v) -> bool:
    return str(v).strip().lower() == "true"


# Very small filterByFormula support: {Field}='Value' (also "=" with double quotes)
_FORMULA_RE = re.compile(r"^\{(?P<field>[^}]+)\}\s*=\s*(['\"])(?P<value>.*)\2$")


class AirtableSession:
    """Deterministic sandbox for the Airtable mock, ported from the FastAPI service.

    Records are modeled generically as {id, createdTime, fields:{...}}. Field
    value casting is driven by the field type declared in the corpus fields
    table (number -> float/int, checkbox -> bool); everything else stays a string.
    """

    def __init__(self, os_cfg, seed=None):
        # Seedless: world loaded verbatim from a frozen snapshot next to
        # this module; `seed` is accepted for client compat and ignored.
        if seed_mode():
            # Seed architecture: world rolled from a seed (re-armed).
            self.rng = random.Random(resolve_seed(seed))
            self.os = connect_os(os_cfg)
            self.time_machine = TimeMachine(rng=self.rng)

            from software.utils.world_data import load_state as _load_state
            _load_state(self, 'LightAirtable')
        else:
            # Seedless: world loaded verbatim from the frozen snapshot.
            restore_into(self, Path(__file__).resolve().parent / "world.pkl")
            self.os = connect_os(os_cfg)

    def _sync_sources(self):
        """apply every change that has landed in this world and this session does not show yet"""
        scope = _task_scope()
        for event in getattr(self, "_task_source_events", []):
            if event.get("applied") or (scope, event["id"]) not in _TASK_LANDED:
                continue
            for item in event["changes"]:
                row = next((r for r in self.records.get(item["table_id"], []) if r["id"] == item["record_id"]), None)
                if row is not None:
                    row["fields"].update(item["fields"])
            event["applied"] = True

    def _count_writes(self, table, n):
        """records written to a table: land every change whose threshold is now reached"""
        scope = _task_scope()
        key = (scope, table["name"])
        _TASK_WRITES[key] = _TASK_WRITES.get(key, 0) + n
        for event in getattr(self, "_task_source_events", []):
            if event["table"] == table["name"] and _TASK_WRITES[key] >= int(event["after"]):
                _TASK_LANDED.add((scope, event["id"]))
        self._sync_sources()

    def get_session_dict(self):
        self._sync_sources()
        return {"records": self.records}

    # --- helpers -----------------------------------------------------------
    def _now(self) -> str:
        return self.os.now()

    def uuid(self) -> str:
        alphabet = "0123456789abcdef"
        return "rec" + ''.join(self.rng.choices(alphabet, k=14))

    def _cast_field(self, table_id, name, value):
        ftype = self._field_types.get(table_id, {}).get(name)
        if value == "" or value is None:
            return None if ftype in ("number",) else value
        if ftype == "number":
            try:
                f = float(value)
                return int(f) if f.is_integer() else f
            except (TypeError, ValueError):
                return value
        if ftype == "checkbox":
            return _to_bool(value)
        return value

    def _coerce_records(self, table_id, rows):
        out = []
        for r in rows:
            fields = {}
            for k, v in r.items():
                if k in ("id", "createdTime"):
                    continue
                cast = self._cast_field(table_id, k, v)
                if cast is None:
                    continue
                fields[k] = cast
            out.append({
                "id": r["id"],
                "createdTime": r["createdTime"],
                "fields": fields,
            })
        return out

    def _resolve_table(self, base_id, table_id_or_name):
        for t in self.tables:
            if t.get("baseId", t.get("base_id")) != base_id:
                continue
            if t["id"] == table_id_or_name or t["name"].lower() == str(table_id_or_name).lower():
                return t
        return None

    def _apply_formula(self, records, formula):
        if not formula:
            return records
        m = _FORMULA_RE.match(formula.strip())
        if not m:
            return records
        field = m.group("field")
        value = m.group("value")
        out = []
        for rec in records:
            fv = rec["fields"].get(field)
            if fv is None:
                continue
            if str(fv) == value:
                out.append(rec)
        return out

    # --- API methods -------------------------------------------------------
    def list_bases(self) -> Dict[str, Any]:
        self._sync_sources()
        return {"status": "ok", "output": {"bases": [{
            "id": b["id"], "name": b["name"],
            "permissionLevel": b.get("permissionLevel", b.get("permission_level")),
        } for b in self.bases]}}

    def list_tables(self, base_id: str) -> Dict[str, Any]:
        if not any(b["id"] == base_id for b in self.bases):
            return {"status": "failed", "output": f"Base {base_id} not found"}
        tables = []
        for t in self.tables:
            if t.get("baseId", t.get("base_id")) != base_id:
                continue
            tables.append({
                "id": t["id"],
                "name": t["name"],
                "primaryFieldId": t.get("primaryFieldId", t.get("primary_field_id", "")),
                "fields": self._field_meta.get(t["id"], []),
            })
        return {"status": "ok", "output": {"tables": tables}}

    def list_records(self, base_id: str, table_id_or_name: str, page_size: int = 100,
                     offset: str | None = None, filter_by_formula: str | None = None) -> Dict[str, Any]:
        self._sync_sources()
        table = self._resolve_table(base_id, table_id_or_name)
        if not table:
            return {"status": "failed", "output": f"Table {table_id_or_name} not found in base {base_id}"}
        records = self.records.get(table["id"], [])
        records = self._apply_formula(records, filter_by_formula)

        page_size = max(1, min(int(page_size), 100))
        try:
            start = int(offset) if offset is not None else 0
        except (TypeError, ValueError):
            start = 0
        page = records[start: start + page_size]
        while len(page) > 1 and len(json.dumps({"records": page}, default=str)) > _PAGE_CHARS:
            page = page[:-1]
        resp = {"records": page}
        next_offset = start + len(page)
        if next_offset < len(records):
            resp["offset"] = str(next_offset)
        return {"status": "ok", "output": resp}

    def get_record(self, base_id: str, table_id_or_name: str, record_id: str) -> Dict[str, Any]:
        self._sync_sources()
        table = self._resolve_table(base_id, table_id_or_name)
        if not table:
            return {"status": "failed", "output": f"Table {table_id_or_name} not found in base {base_id}"}
        for rec in self.records.get(table["id"], []):
            if rec["id"] == record_id:
                return {"status": "ok", "output": rec}
        return {"status": "failed", "output": f"Record {record_id} not found"}

    def create_records(self, base_id: str, table_id_or_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        self._sync_sources()
        table = self._resolve_table(base_id, table_id_or_name)
        if not table:
            return {"status": "failed", "output": f"Table {table_id_or_name} not found in base {base_id}"}
        created = []
        rows = self.records.setdefault(table["id"], [])
        for item in records:
            fields = item.get("fields", {}) or {}
            rec = {
                "id": self.uuid(),
                "createdTime": self._now(),
                "fields": dict(fields),
            }
            rows.append(rec)
            created.append(rec)
        self._count_writes(table, len(created))
        return {"status": "ok", "output": {"records": created}}

    def update_record(self, base_id: str, table_id_or_name: str, record_id: str,
                      fields: Dict[str, Any]) -> Dict[str, Any]:
        self._sync_sources()
        table = self._resolve_table(base_id, table_id_or_name)
        if not table:
            return {"status": "failed", "output": f"Table {table_id_or_name} not found in base {base_id}"}
        for rec in self.records.get(table["id"], []):
            if rec["id"] == record_id:
                rec["fields"] = {**rec["fields"], **(fields or {})}
                self._count_writes(table, 1)
                return {"status": "ok", "output": rec}
        return {"status": "failed", "output": f"Record {record_id} not found"}

    def delete_record(self, base_id: str, table_id_or_name: str, record_id: str) -> Dict[str, Any]:
        self._sync_sources()
        table = self._resolve_table(base_id, table_id_or_name)
        if not table:
            return {"status": "failed", "output": f"Table {table_id_or_name} not found in base {base_id}"}
        rows = self.records.get(table["id"], [])
        for i, rec in enumerate(rows):
            if rec["id"] == record_id:
                rows.pop(i)
                return {"status": "ok", "output": {"id": record_id, "deleted": True}}
        return {"status": "failed", "output": f"Record {record_id} not found"}


if __name__ == "__main__":
    s = AirtableSession(seed=12)
    print(s.list_bases())
    print(s.list_tables("appNW1studio0001"))
