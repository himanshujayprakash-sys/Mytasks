# Shared helpers. Sourced after config.sh.

log() { echo "[$(date +%H:%M:%S)] $*"; }
die() { echo "[pipeline] ERROR: $*" >&2; exit 1; }

# batch_dir <batch>: the batch's folder (must exist).
batch_dir() {
  local d="$PIPELINE/batches/$1"
  [ -d "$d" ] || die "no batch '$1' (create it with: pipeline.sh new $1 <tasks folder>)"
  echo "$d"
}

# batch_tasks <batch> [uuid ...]: the given uuids, or every task in the batch.
batch_tasks() {
  local b="$1"; shift
  if [ $# -gt 0 ]; then printf '%s\n' "$@"; return; fi
  (cd "$PIPELINE/batches/$b/tasks" && ls -d *-*-*-*-*/ 2>/dev/null | tr -d /)
}

# fingerprint <dir>: sha256 of the task's content (trajectories/ excluded), the same on any laptop.
fingerprint() { "$PY" "$PIPELINE/lib/fingerprint.py" "$1"; }

# gate_hash <batch> <uuid>: the fingerprint the gate-1 verdict was given to.
gate_hash() {
  local g="$PIPELINE/batches/$1/1_qc/$2/gate.json"
  [ -f "$g" ] && "$PY" -c 'import json,sys;print(json.load(open(sys.argv[1])).get("task_sha256",""))' "$g"
}

# gate_verdict <batch> <uuid>: PASS / FAIL / PENDING from 1_qc/<uuid>/gate.json, or CHANGED when the task's files
# are no longer the ones that verdict was given to (an edit after QC, e.g. a hardening round): a CHANGED task is
# never run, packaged or delivered until gate 1 runs again on the new files.
gate_verdict() {
  local g="$PIPELINE/batches/$1/1_qc/$2/gate.json"
  [ -f "$g" ] || { echo PENDING; return; }
  local v; v=$("$PY" -c 'import json,sys;print(json.load(open(sys.argv[1]))["verdict"])' "$g")
  if [ "$v" != PENDING ] && [ "$(gate_hash "$1" "$2")" != "$(fingerprint "$PIPELINE/batches/$1/tasks/$2")" ]; then
    echo CHANGED; return
  fi
  echo "$v"
}

# changed_files <batch> <uuid>: which files differ from the ones gate 1 checked.
changed_files() {
  "$PY" -c '
import json, sys
sys.path.insert(0, sys.argv[3])
import fingerprint
old = json.load(open(sys.argv[1]))["files"]; new = fingerprint.files(__import__("pathlib").Path(sys.argv[2]))
for k in sorted(set(old) | set(new)):
    if old.get(k) != new.get(k): print("  " + ("added   " if k not in old else "removed " if k not in new else "changed ") + k)
' "$PIPELINE/batches/$1/1_qc/$2/qc_fingerprint.json" "$PIPELINE/batches/$1/tasks/$2" "$PIPELINE/lib"
}

# Keep model / judge credentials out of a process (the QC hard rules); the judged runs add the codex login back.
scrub_env() {
  unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN OPENAI_API_KEY GEMINI_API_KEY
  unset JUDGE_CLAUDE_TOKEN CLAUDE_CODE_OAUTH_TOKEN CODEX_AUTH_B64 JUDGE_DOCKERFILE LIGHT_SERVERS_DOCKERFILE
}
