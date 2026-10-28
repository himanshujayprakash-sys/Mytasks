#!/bin/bash
# hma_build.sh <task dir> [...]: build tasks with harness_mcp_atlas (the harness that makes the stage-1 trajectories),
# so QC runs on exactly the files that run and ship. Per task:
#   1. import_task --force: the author-owned half becomes input/<uuid> (the harness drops its own verifier files)
#   2. keep the task's contamination-screen roots/ and .identity.json from the user's existing input folder
#   3. validate, then build -> $HMA_MAIN/out/build/<uuid>
# Never writes in <task dir>. HMA_MAIN is a separate checkout of harness_mcp_atlas origin/main (the user's own
# checkout and its local edits are never touched).
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
source "$HERE/config.sh"; source "$HERE/lib/common.sh"
HMA_MAIN="${HMA_MAIN:-$DELIVERY/harness_mcp_atlas_main}"
[ -x "$HMA_MAIN/.venv/bin/python" ] || die "no $HMA_MAIN/.venv (see pipeline/README.md: harness_mcp_atlas_main)"
rc=0
for SRC in "$@"; do
  SRC="$(cd "$SRC" && pwd)"; U=$(basename "$SRC"); I="$HMA_MAIN/input/$U"
  (cd "$HMA_MAIN" && .venv/bin/python -m harness.import_task --from "$SRC" --name "$U" --force) > "$HMA_MAIN/out/import_$U.log" 2>&1 \
    || { log "$U: import failed ($HMA_MAIN/out/import_$U.log)"; rc=1; continue; }
  # contamination-screen roots: the task set's own _roots/<uuid> (written by tools/screen_task.py), else the user's
  # existing harness input folder
  if [ -d "$(dirname "$SRC")/_roots/$U" ]; then rm -rf "$I/roots"; cp -R "$(dirname "$SRC")/_roots/$U" "$I/roots"
  elif [ ! -d "$I/roots" ] && [ -d "$HMA/input/$U/roots" ]; then cp -R "$HMA/input/$U/roots" "$I/roots"; fi
  v=$(cd "$HMA_MAIN" && .venv/bin/python -m harness.cli --task "input/$U" --only validate 2>&1)
  echo "$v" | grep -q "input ok" || { log "$U: validate FAILED:"; echo "$v" | grep -iE "error|refus|fail" | head -5; rc=1; continue; }
  echo "$v" | grep "WARNING" | sed "s/^/  /"
  b=$(cd "$HMA_MAIN" && .venv/bin/python -m harness.cli --task "input/$U" --only build 2>&1)
  echo "$b" | grep -q "built " || { log "$U: build FAILED:"; echo "$b" | tail -5; rc=1; continue; }
  log "$U: built -> $HMA_MAIN/out/build/$U ($(fingerprint "$HMA_MAIN/out/build/$U" | cut -c1-12))"
done
exit $rc
