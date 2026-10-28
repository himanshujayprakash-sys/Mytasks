#!/bin/bash
# laptop2_bundle.sh <uuid> [...]: pack the harness inputs of tasks that passed static QC here, for a second laptop that only runs
# trajectories (harness_mcp_atlas d731e75, opus-5, effort high). Each file is listed with its SHA-256 so that laptop checks it
# runs byte for byte the files QC passed; its packaged results come back here and gate 2's lock check catches any drift.
# Output: $DELIVERY/to_laptop2/inputs_<stamp>.tar.gz and the same name with .sha256 (one line per file, relative to input/).
set -uo pipefail
source "$(dirname "$0")/../config.sh"; source "$(dirname "$0")/../lib/common.sh"
HMA_MAIN="${HMA_MAIN:-$DELIVERY/harness_mcp_atlas_main}"; BATCH="${BATCH:-v2_20261028}"
[ $# -gt 0 ] || die "usage: laptop2_bundle.sh <uuid> [...]"
OUT="$DELIVERY/to_laptop2"; mkdir -p "$OUT"; STAMP=$(date +%Y%m%d-%H%M); TAR="$OUT/inputs_$STAMP.tar.gz"
for U in "$@"; do
  [ -d "$HMA_MAIN/input/$U" ] || die "$U: no harness input (run tools/hma_build.sh first)"
  [ "$(gate_verdict "$BATCH" "$U" 2>/dev/null)" = PASS ] || log "WARNING $U: gate 1 is not PASS in $BATCH; check the static QC first"
done
(cd "$HMA_MAIN/input" && find "$@" -type f ! -name .DS_Store ! -path '*/__pycache__/*' -print0 | sort -z | xargs -0 shasum -a 256) > "${TAR%.tar.gz}.sha256"
(cd "$HMA_MAIN/input" && COPYFILE_DISABLE=1 tar czf "$TAR" --exclude .DS_Store --exclude __pycache__ "$@")
log "packed $# task(s): $TAR ($(du -h "$TAR" | cut -f1)), $(wc -l < "${TAR%.tar.gz}.sha256" | tr -d ' ') files listed in ${TAR%.tar.gz}.sha256"
