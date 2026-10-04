#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# tmsel_probes.sh: the store arms' named TM_SEL encoding (srp_store_wrap.sv
# TB_TM_SEL_C = 1'b0) against two disposable edits, each in a fresh
# `git archive` of the head, `make storage` at 1x1 and 9x9:
#  recode : KL_srp_top's tm_st_e re-encoded TM_SEL = 1'b1, TM_POP = 1'b0, a
#           behaviour-neutral RTL edit; the wrap's named encoding is then
#           stale, and the arms must fail loudly rather than pass silently;
#  hierref: the wrap names the enum item through the hierarchy instead
#           (u_dut.TM_SEL), the form the wrap says the simulator faults on.
set -u
P=${P:-$(cd "$(dirname "$0")/.." && pwd)}
. "$P/scripts/env.sh"
CLONE=${CLONE:?set CLONE to a clone that holds the exact head}
T=$S/tmsel; rm -rf "$T"; mkdir -p "$T"
for v in recode hierref; do
  mkdir -p "$T/$v"; git -C "$CLONE" archive "$HEAD" hdl tb/common tb/srp_top | tar -x -C "$T/$v"
done
python3 - "$T" <<'PY'
import pathlib, sys
T = pathlib.Path(sys.argv[1])
p = T / "recode/hdl/srp/KL_srp_top.sv"; s = p.read_text()
a = "    TM_SEL = 1'b0,"; b = "    TM_POP = 1'b1    // issue"
assert s.count(a) == 1 and s.count(b) == 1
s = s.replace(a, "    TM_SEL = 1'b1,").replace(b, "    TM_POP = 1'b0    // issue")
p.write_text(s)
p = T / "hierref/tb/srp_top/srp_store_wrap.sv"; s = p.read_text()
a = "localparam logic TB_TM_SEL_C = 1'b0;"; assert s.count(a) == 1
p.write_text(s.replace(a, "localparam logic TB_TM_SEL_C = u_dut.TM_SEL;"))
PY
for v in recode hierref; do for sh in 1x1 9x9; do
  echo "$v $sh"
done; done | xargs -P 4 -L 1 bash -c 'd='"$T"'/$0; make -C "$d/tb/srp_top" storage SHAPE=$1 > "$d/$1.log" 2>&1; echo $? > "$d/$1.rc"'
for v in recode hierref; do for sh in 1x1 9x9; do
  d=$T/$v
  printf '%s %s rc=%s fails=%s | %s | %s\n' "$v" "$sh" "$(cat "$d/$sh.rc")" "$(grep -c '^FAIL' "$d/$sh.log")" \
    "$(grep 'checks:' "$d/$sh.log" | tail -1)" "$(grep -m1 -i 'segmentation\|internal error\|%Error' "$d/$sh.log" | cut -c1-160)"
done; done
