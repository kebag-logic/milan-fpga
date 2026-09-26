#!/usr/bin/env bash
# Export exact base, round-2 head and round-3 head trees into disposable scratch
# copies (the clone stays untouched). Parallelism only: cap Verilator build jobs at 8.
set -euo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); C=${CLONE:-$REVIEWS/r334-2-pp120}
for n in base:0922e43408f891fc0b84a84691df86b4fd0f1c0d r2:a9b7874d415d935949becd7ccfd58799927efb08 head:83c84b19e09d397ed2eb6f5ace337686ce0ef86b; do
  d=$PK/scratch/${n%%:*}; rm -rf "$d"; mkdir -p "$d"
  git -C "$C" archive "${n#*:}" | tar -x -C "$d"
  sed -i 's/--build -j 0/--build -j 8/' "$d/tb/pp_top/Makefile"
  echo "exported ${n%%:*} ${n#*:}"
done
