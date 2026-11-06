#!/bin/bash
# Gather this session's receipts from scratch into the packet: small text as it is, large logs as a digest and a tail.
# Host paths are replaced by role placeholders in make_index.py. Re-run after each stage.
set -u
O=$MANAGEMENT/2026-09-23/665s4-a698i; S=$VALIDATION_STORAGE/scratch/665s4-a698i; R=$O/receipts
small() { # small SRC DST: the file, or its digest and tail when over the packet's limit
  mkdir -p "$(dirname "$2")"
  python3 -I - "$1" "$2" <<'PY'
import hashlib, sys
from pathlib import Path
src, dst = map(Path, sys.argv[1:])
data = src.read_bytes()
if len(data) > 150000:
    data = (f'FULL LOG: bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}\nTAIL:\n').encode() + data[-60000:]
dst.write_bytes(data)
PY
}
for n in image-selftest firmware_boundary firmware_boundary_verilator boot-1x1 boot-8x8 partial-map-probe map-edges py-idiom identity mutants2; do
  [ -f "$S/$n.log" ] && small "$S/$n.log" "$R/runs/$n.log"
  [ -f "$S/$n.rc" ] && cp "$S/$n.rc" "$R/runs/$n.rc"
  [ -f "$S/$n.peak" ] && cp "$S/$n.peak" "$R/runs/$n.peak"
done
[ -f "$S/image-hashes.txt" ] && cp "$S/image-hashes.txt" "$R/runs/image-hashes.txt"
[ -f "$S/mutants.md" ] && cp "$S/mutants.md" "$R/mutants.md"
for f in "$S"/kept/*; do [ -f "$f" ] && small "$f" "$R/kept/$(basename "$f")"; done
for f in "$S"/mutants/*.log; do [ -f "$f" ] && small "$f" "$R/mutants/$(basename "$f")"; done
if [ -d "$S/docs-final/logs" ]; then
  mkdir -p "$R/docs"
  for f in "$S"/docs-final/logs/*; do small "$f" "$R/docs/$(basename "$f")"; done
  [ -f "$S/docs-final/docs-yml-table.md" ] && small "$S/docs-final/docs-yml-table.md" "$R/docs/docs-yml-table.md"
  [ -f "$S/docs-final/runner.out" ] && small "$S/docs-final/runner.out" "$R/docs/runner.out"
  [ -f "$S/docs-final/verify.rc" ] && cp "$S/docs-final/verify.rc" "$R/docs/verify.rc"
fi
