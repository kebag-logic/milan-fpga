#!/bin/sh
# Usage: probe_build.sh <scratch-copy-of-clone> <receipt-dir> <shim-bin-dir>
# Builds the clean shipping elaboration and five disposable variants of it in
# a SCRATCH copy of the reviewed head, one object directory each:
#   nodwell  harness: the #657 epoch-only boot dwell removed
#   noburst  harness: the #657 double-rate burst never raised
#   frozen   RTL: the campaign's "uncounted repeat" edit (counter frozen)
#   plus2    RTL: each underrun counted twice
#   sat3     RTL: the underrun counter saturates at 3
# Every edit is asserted to match exactly once; the harness file is restored
# from git after each harness variant.
set -u
copy=$1; out=$2; bin=$3
export PATH="$bin:$PATH" VERILATOR="$bin/verilator" VERILATOR_JOBS=4
d="$copy/tb/verilator/milan_dp_render"
rtl="$copy/hdl/ieee1722/aaf/KL_tdm_render_master.sv"
mut="$copy/../mut"; mkdir -p "$mut"
cd "$d" || exit 99
log="$out/probe_build.log"; : > "$log"

edit() {  # edit <file-in> <file-out> <old> <new>
python3 -I - "$1" "$2" "$3" "$4" <<'EOF'
import sys
src, dst, old, new = sys.argv[1:]
t = open(src).read()
n = t.count(old)
if n != 1:
    sys.exit(f"anchor matched {n} times in {src}")
open(dst, "w").write(t.replace(old, new))
EOF
}

b() {  # b <mdir> [extra make args]
  m=$1; shift
  echo "== build $m $*" >> "$log"
  taskset -c 6-11 make --no-print-directory -s tdm8render-build TDM8R_MDIR="$m" "$@" >> "$log" 2>&1
  echo "== build $m rc=$?" >> "$log"
}

b obj_p_clean

H=sim_tdm8_render.cpp
edit "$H" "$H" "    if (epoch_only) run_fed(kBootPullInCycles);
" "" && b obj_p_nodwell
git checkout -- "$H"
edit "$H" "$H" "    tdm_double_rate = true;" "    tdm_double_rate = false;" && b obj_p_noburst
git checkout -- "$H"
git diff --quiet -- "$H" || echo "HARNESS NOT RESTORED" >> "$log"

L="          else unders_b_r <= (&unders_b_r) ? unders_b_r : unders_b_r + 16'd1;"
edit "$rtl" "$mut/frozen.sv" "$L" "          else unders_b_r <= unders_b_r;" &&
  b obj_p_frozen TDMRM_SRC="$mut/frozen.sv"
edit "$rtl" "$mut/plus2.sv" "$L" "          else unders_b_r <= (&unders_b_r) ? unders_b_r : unders_b_r + 16'd2;" &&
  b obj_p_plus2 TDMRM_SRC="$mut/plus2.sv"
edit "$rtl" "$mut/sat3.sv" "$L" "          else unders_b_r <= (&unders_b_r[1:0]) ? unders_b_r : unders_b_r + 16'd1;" &&
  b obj_p_sat3 TDMRM_SRC="$mut/sat3.sv"
git -C "$copy" status --short --untracked-files=no >> "$log"
echo "== probe builds done" >> "$log"
