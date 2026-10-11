#!/bin/sh
# Reviewer reproduction for R616-2 (FPGA-gPTP PR #80 at a70e38804cb16435c089d024c58e8c3fb4d39ff6).
# usage: reproduce.sh <clone-at-a70e388> <work-dir> <receipts-dir>
# Needs: pinned Verilator 5.050 as `verilator` on PATH (scripts/verilator_jcap.sh
# caps the build's -j 0 at 4), python3, yosys, sv2v.
set -u
clone=$1; S=$2; R=$3; here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$S/head" "$S/base" "$S/hb" "$R"
git -C "$clone" archive a70e38804cb16435c089d024c58e8c3fb4d39ff6 | tar -x -C "$S/head"
git -C "$clone" archive 5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d | tar -x -C "$S/base"
cp -a "$S/head/." "$S/hb/"; cp "$S/base/hdl/wire/KL_gptp_rx_parser.sv" "$S/hb/hdl/wire/"
r() { n=$1; d=$2; shift 2; ( cd "$d" && "$@" >"$R/$n.log" 2>&1; echo $? >"$R/$n.rc" ) & }
r head_parser "$S/head" make -C tb/verilator/parser run
r head_parser_mutants "$S/head/tb/verilator/parser" python3 mutants.py
r baseRTL_headbench_parser "$S/hb" make -C tb/verilator/parser run
r baseRTL_parser_mutants "$S/hb/tb/verilator/parser" python3 mutants.py
r base_parser "$S/base" make -C tb/verilator/parser run
r head_lint "$S/head" make lint
r head_docs "$S/head" make docs
r head_contract "$S/head" make contract
wait
r head_engine "$S/head" make -C tb/verilator/engine run
r head_tsngen "$S/head" make -C tb/tsngen
r head_bench "$S/head" make -C bench/arty test
( VERILATOR=verilator "$here/probe.sh" "$S/head" "$S/probe_head" >"$R/probe_head.log" 2>&1; echo $? >"$R/probe_head.rc" ) &
( VERILATOR=verilator "$here/probe.sh" "$S/base" "$S/probe_base" >"$R/probe_base.log" 2>&1; echo $? >"$R/probe_base.rc" ) &
wait
# padding mutant: the latch ignores rx_err_i on bytes past the declared messageLength
cp -a "$S/head" "$S/mpad"; rm -rf "$S/mpad/tb/verilator/parser/obj_dir"
python3 - "$S/mpad/hdl/wire/KL_gptp_rx_parser.sv" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read(); old="        if (rx_err_i) bad_r <= 1'b1;\n"
assert t.count(old)==1
open(p,'w').write(t.replace(old,"        if (rx_err_i && (rx_sof_i || cnt_r <= 11'(OFF_MSGLEN_END_C) || cnt_r <= msg_end_r)) bad_r <= 1'b1;\n"))
PY
r mutant_pad_author_suite "$S/mpad" make -C tb/verilator/parser run
( VERILATOR=verilator "$here/probe.sh" "$S/mpad" "$S/probe_mpad" >"$R/mutant_pad_probe.log" 2>&1; echo $? >"$R/mutant_pad_probe.rc" ) &
"$here/equiv.sh" "$S/base" "$S/head" "$S/equiv" >"$R/equiv.log" 2>&1
wait
