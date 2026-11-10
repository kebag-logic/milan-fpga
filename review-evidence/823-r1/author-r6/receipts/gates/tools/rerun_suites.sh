#!/usr/bin/env bash
# rerun_suites.sh <outdir> <suite>...: from the root of a clean clone, re-run the sweep suites the wall
# clock killed, one at a time, exactly as scripts/run_all_suites.sh runs one: its own suite_timeout (read
# from the script, not copied), `timeout <T> make -C tb/verilator/<suite>`, and the masked-verdict check
# (scripts/suite_tally.py --verdict); then the tally over the re-run logs. Exit 0 only when every suite
# passed and the tally read every count.
set -u
OUT=$1; shift; mkdir -p "$OUT"; worst=0
eval "$(sed -n '/^suite_timeout() {/,/^}/p' scripts/run_all_suites.sh)"
for s in "$@"; do
  T=$(suite_timeout "$s"); start=$(date +%s)
  timeout "$T" make -C "tb/verilator/$s" > "$OUT/$s.log" 2>&1; rc=$?
  if [ "$rc" -eq 0 ] && ! v=$(python3 scripts/suite_tally.py --verdict "$OUT/$s.log" 2>&1); then
    rc=93; printf '%s\n' "$v"
  fi
  echo "$s rc=$rc wall=$(( $(date +%s) - start ))s timeout=${T}s"
  [ "$rc" -ne 0 ] && worst=1
done
python3 scripts/suite_tally.py "$OUT" --quiet || worst=1
exit "$worst"
