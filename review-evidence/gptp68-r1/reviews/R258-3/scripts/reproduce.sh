#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reproduce the R258-3 receipts from a clone of Mister-M-alt/FPGA-gPTP.
# Every build and run happens in exports under $WORK; the clone is only read.
#
# env: CLONE      the FPGA-gPTP clone (must hold the four commits below)
#      WORK       a disposable directory
#      VERILATOR  the Verilator 5.050 wrapper
#      PARENT     a directory holding the six parent files listed in
#                 receipts/inputs.txt at their paths (fetched at parent live
#                 dev 759da623 and checked against those blob ids)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
: "${CLONE:?}" "${WORK:?}" "${VERILATOR:?}" "${PARENT:?}"
export VERILATOR
HEAD=ba9268100ebe92dfc61aed30e2910245fc8c97cf
BASE=c1b617435824929a790739ea8585c3fe1a328cc0
PRIOR=cbccf226068c107fb30764891c98b8d70c54d775
FIRST=77c34e904eba2446755d13e1bf4763d1652c3ca7
mkdir -p "$WORK"
for pair in head:$HEAD base:$BASE cbccf22:$PRIOR c77:$FIRST; do
  d="$WORK/${pair%%:*}"; mkdir -p "$d"
  git -C "$CLONE" archive "${pair#*:}" | tar -x -C "$d"
done

# ROM regeneration and program-level content diff
for t in head base cbccf22; do sh "$HERE/rom_check.sh" "$WORK/$t" "$WORK/rom_$t"; done
python3 "$HERE/rom_program_diff.py" "$WORK/base/hdl/ucode/gen_gptp_ucode.py" \
  "$WORK/head/hdl/ucode/gen_gptp_ucode.py" --clk-hz 2000000 --cease-ms 3000

# engine suite, three images
sh "$HERE/engine_suite.sh" "$WORK/head" "$WORK/eng_head"

# the suite's own mutation arm in four slices (Verilator must be on PATH)
PATH=$(dirname "$VERILATOR"):$PATH
export PATH TMPDIR="$WORK"
for k in 0 1 2 3; do
  python3 "$HERE/mutant_slices.py" "$WORK/head" own "$k" 4 2 &
done
wait

# per-check attribution, reviewer mutants, older generators
python3 "$HERE/mutant_failures.py" "$WORK/head" \
  "$WORK/eng_head/obj_dir/Vengine_sim" "$WORK/mfail" \
  "base_c1b6174=$WORK/base/hdl/ucode/gen_gptp_ucode.py" \
  "77c34e9=$WORK/c77/hdl/ucode/gen_gptp_ucode.py" \
  "cbccf22=$WORK/cbccf22/hdl/ucode/gen_gptp_ucode.py"

# reviewer scenario probes PX1-PX6 on the head image and on controls
M="$WORK/mfail"
sh "$HERE/build_probe.sh" "$WORK/head" "$WORK/probe" \
  "R2_fall_rearms=$M/reviewer__R2_the_asCapable_fall_re_arms_instead_of_the_rise/gen.py" \
  "cbccf22=$WORK/cbccf22/hdl/ucode/gen_gptp_ucode.py" \
  "timeout_unlocks=$M/own__a_receipt_timeout_unlocks_the_servo/gen.py" \
  "become_unlocks=$M/own__becoming_grandmaster_unlocks_the_servo/gen.py" \
  "rise_keeps_lock=$M/own__asCapable_s_rise_keeps_the_lock/gen.py"

# the parent's gptp_plane suite against three donors
for t in head base cbccf22; do
  sh "$HERE/parent_gptp_plane.sh" "$PARENT" "$WORK/$t" "$WORK/pp_$t"
done

# clone integrity
sh "$HERE/clone_integrity.sh" "$CLONE" "$HEAD" \
  5a02fa35db15d9a773895f82bb17020b55cfa775
