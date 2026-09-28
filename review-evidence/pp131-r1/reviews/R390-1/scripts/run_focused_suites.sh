#!/bin/sh
# Reviewer run of the 18.1-named focused suites at the exact head, in a
# disposable git-archive copy. Usage: run_focused_suites.sh <clone> <out> <verilator>
set -u
HEAD=${HEAD:-e1ae468f7e237f321ce5fee19e59ae157da4b83d}
SRC=$1; OUT=$2; VL=$3
rm -rf "$OUT"; mkdir -p "$OUT"
git -C "$SRC" archive "$HEAD" | tar -x -C "$OUT"
for suite in acmp_nvm nvm_port desc_mem_guard dyn_state desc_store lsn_admit adp_engine; do
  ( cd "$OUT/tb/$suite" && make VERILATOR="$VL" > "$OUT/$suite.log" 2>&1 ); rc=$?
  echo "suite $suite rc=$rc: $(tail -1 "$OUT/$suite.log")"
done
