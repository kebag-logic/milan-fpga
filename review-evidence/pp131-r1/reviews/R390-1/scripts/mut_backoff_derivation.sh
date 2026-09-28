#!/bin/sh
# Reviewer mutant: change the top's product backoff derivation
# ceil(CLK_HZ_P / 2) to CLK_HZ_P / 200 (5 ms) in a disposable copy and run
# the suites that instantiate the top. SURVIVED = every suite still passes.
set -u
HEAD=${HEAD:-e1ae468f7e237f321ce5fee19e59ae157da4b83d}
SRC=$1; OUT=$2; VL=$3
rm -rf "$OUT"; mkdir -p "$OUT"
git -C "$SRC" archive "$HEAD" | tar -x -C "$OUT"
F="$OUT/hdl/top/protocol_processor_top.sv"
python3 - "$F" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2),"
new = "NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd200),"
assert s.count(old) == 1, "anchor"
open(p, "w").write(s.replace(old, new))
PY
rc_all=0
for suite in pp_top timer_map; do
  ( cd "$OUT/tb/$suite" && make VERILATOR="$VL" > "$OUT/$suite.log" 2>&1 ); rc=$?
  echo "mutant backoff_derivation suite $suite rc=$rc: $(tail -1 "$OUT/$suite.log")"
  [ $rc -ne 0 ] && rc_all=1
done
if [ $rc_all -eq 0 ]; then echo "VERDICT backoff_derivation SURVIVED"; else echo "VERDICT backoff_derivation KILLED"; fi
