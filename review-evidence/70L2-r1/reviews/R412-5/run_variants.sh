#!/bin/sh
# Build and run every probe variant in stop mode, at most 8 at a time.
# Usage: run_variants.sh [variant ...]   (default: all but H0_head)
cd "$(dirname "$0")" || exit 2
if [ $# -eq 0 ]; then
  set -- $(python3 -c 'import probe_lib; print(" ".join(k for k in probe_lib.VARIANTS if k != "H0_head"))')
fi
printf '%s\n' "$@" | xargs -P 8 -I{} sh -c \
  'python3 probe_lib.py {} >/dev/null && python3 run_gate1b.py scratch/v/{} stop > receipts/{}.stop.log 2>&1; echo "{} rc=$?" >> receipts/{}.stop.log'
for v in "$@"; do
  printf '%-36s %s | %s\n' "$v" "$(grep -E '^GATE1B' receipts/$v.stop.log | cut -c1-230)" \
    "$(grep -E '^R412 STOP' receipts/$v.stop.log)"
done
