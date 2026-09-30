#!/bin/sh
# Build each named variant and run the WHOLE gate-1b function (no stop), 8 at a time.
cd "$(dirname "$0")" || exit 2
printf '%s\n' "$@" | xargs -P 8 -I{} sh -c \
  'python3 probe_lib.py {} >/dev/null && python3 run_gate1b.py scratch/v/{} > receipts/{}.whole.log 2>&1; echo "{} rc=$?" >> receipts/{}.whole.log'
for v in "$@"; do
  printf '%-36s %s\n' "$v" "$(grep -E '^GATE1B' receipts/$v.whole.log | cut -c1-400)"
done
