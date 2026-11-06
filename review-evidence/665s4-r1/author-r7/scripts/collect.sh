#!/bin/bash
# Gather this session's receipts from scratch into the packet: small text as it is, large logs as a digest and a tail.
# Host paths are replaced by role placeholders in make_index.py. Re-run after each stage.
set -u
O=$MANAGEMENT/2026-09-23/665s4-a698h; S=$VALIDATION_STORAGE/scratch/665s4-a698h; R=$O/receipts
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
for n in boot-1x1 boot-8x8 boot-selftest placement-1x1 placement-8x8 nomap-probe page-plat map-8x8 page-design refusal-probe \
         nvm-capture py-idiom image-selftest firmware_boundary_verilator firmware_boundary mutants base-1x1 dev-8x8; do
  [ -f "$S/$n.log" ] && small "$S/$n.log" "$R/runs/$n.log"
  [ -f "$S/$n.rc" ] && cp "$S/$n.rc" "$R/runs/$n.rc"
  [ -f "$S/$n.peak" ] && cp "$S/$n.peak" "$R/runs/$n.peak"
done
for f in "$S"/kept/*; do [ -f "$f" ] && small "$f" "$R/kept/$(basename "$f")"; done
for f in "$S"/mutants/*.log; do [ -f "$f" ] && small "$f" "$R/mutants/$(basename "$f")"; done
[ -f "$S/mutants/true-map-boot/soc-provisional.log" ] && tail -1 "$S/mutants/true-map-boot/soc-provisional.log" > "$R/mutants/guard-refuses-a-true-map-cause.txt"
[ -f "$S/nomap-probe-out.log" ] && small "$S/nomap-probe-out.log" "$R/runs/nomap-probe-builder.log"
[ -f "$S/page-plat/fence.log" ] && small "$S/page-plat/fence.log" "$R/runs/page-plat-fence.log"
[ -f "$S/page-design/fence.log" ] && small "$S/page-design/fence.log" "$R/runs/page-design-fence.log"
if [ -d "$S/docs-final/logs" ]; then
  mkdir -p "$R/docs"
  for f in "$S"/docs-final/logs/*; do small "$f" "$R/docs/$(basename "$f")"; done
  [ -f "$S/docs-final/docs-yml-table.md" ] && small "$S/docs-final/docs-yml-table.md" "$R/docs/docs-yml-table.md"
  [ -f "$S/docs-final/runner.out" ] && small "$S/docs-final/runner.out" "$R/docs/runner.out"
  [ -f "$S/docs-final/verify.rc" ] && cp "$S/docs-final/verify.rc" "$R/docs/verify.rc"
fi
