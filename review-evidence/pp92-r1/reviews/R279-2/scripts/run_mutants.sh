#!/usr/bin/env bash
# Reviewer mutation probes (R279-2) on disposable copies of the exact head.
# Each mutant is one textual edit, asserted to apply exactly once; each copy
# builds the pp_top DEFAULT build (the one that runs sections BW0-BW4) or the
# acmp_nvm bench, and the tally/FAIL lines are recorded.
# usage: run_mutants.sh <review clone> <packet dir> <verilator wrapper>
set -uo pipefail
CLONE=$1; PKT=$2; VER=$3
export PATH="$(dirname "$VER"):$PATH"
SCR=$PKT/scratch/mut
HEAD=f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3
mkdir -p "$SCR"
mk() {  # mk <name> <file> <python old> <python new>
  rm -rf "$SCR/$1"; mkdir -p "$SCR/$1"
  git -C "$CLONE" archive $HEAD | tar -x -C "$SCR/$1"
  [ -z "$2" ] && return 0
  python3 - "$SCR/$1/$2" "$3" "$4" <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
old = sys.argv[2].encode().decode('unicode_escape'); new = sys.argv[3].encode().decode('unicode_escape')
assert s.count(old) == 1, (p, s.count(old))
p.write_text(s.replace(old, new))
EOF
}
pptop() {  # default pp_top build + run, in tree $1
  ( cd "$SCR/$1/tb/pp_top" && python3 ../../hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex >/dev/null \
    && python3 ../../hdl/aecp/ucode/gen_ucode.py -o ucode.hex >/dev/null \
    && srcs=$(make -s -p -n run 2>/dev/null | sed -n 's/^SRCS = //p' | head -1) \
    && srcs=$(echo "$srcs" | sed 's#\$(HDL)#../../hdl#g') \
    && verilator --cc --exe --build -j 2 --top-module pp_top_wrap -Wall -Wno-fatal \
       -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
       -CFLAGS "-std=c++17 -O2 -I$PWD -Wall -Wextra" $srcs sim_main.cpp -o Vpp_top_sim >build.log 2>&1 \
    && ./obj_dir/Vpp_top_sim > run.log 2>&1; echo "exit $?" >> run.log )
}
acmp() {  # acmp_nvm bench, target $2 (run|pinned), in tree $1
  ( cd "$SCR/$1/tb/acmp_nvm" && make "$2" > run.log 2>&1; echo "exit $?" >> run.log )
}
OLDCMP_NEW="  assign c1_diff_w  = (c1_vld_r != valid_r[c1_sink_r])\n                    || (c1_vld_r && (SHW_W_C'(c1_proj_r) != cmp_data_w));"
OLDCMP_OLD="  assign c1_diff_w  = (SHW_W_C'(c1_proj_r) != cmp_data_w)\n                    || (c1_vld_r != valid_r[c1_sink_r]);"
mk pt-head "" "" ""
mk pt-oldcmp hdl/acmp/KL_acmp_nvm_shadow.sv "$OLDCMP_NEW" "$OLDCMP_OLD"
mk pt-done-norel hdl/top/protocol_processor_top.sv \
  "assign restore_done_o = nvm_walk_done_w && lsn_released_w;" "assign restore_done_o = nvm_walk_done_w;"
mk pt-busy-nogap hdl/top/protocol_processor_top.sv \
  "  assign restore_busy_o = nvm_walk_busy_w\n                          || (nvm_walk_done_w && !lsn_released_w);" \
  "  assign restore_busy_o = nvm_walk_busy_w;"
mk an-pinned "" "" ""
pptop pt-head & pptop pt-oldcmp & pptop pt-done-norel & pptop pt-busy-nogap & acmp an-pinned pinned &
wait
for t in pt-head pt-oldcmp pt-done-norel pt-busy-nogap; do
  echo "=== $t (pp_top default build)"
  grep -E '^FAIL|checks|^exit' "$SCR/$t/tb/pp_top/run.log" | head -20
done
echo "=== an-pinned (acmp_nvm pinned control)"
grep -cE '^FAIL' "$SCR/an-pinned/tb/acmp_nvm/run.log"
grep -E '^FAIL: L05a|checks:|^exit' "$SCR/an-pinned/tb/acmp_nvm/run.log"
