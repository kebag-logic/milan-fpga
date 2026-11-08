#!/usr/bin/env bash
# R792-2 probe runs at PR #853 head 526f937c, as executed (each step is a foreground command; the
# independent ones were started together and waited on). Usage: run_probes.sh <clone> <packet>
# <clone>: a clean checkout of 526f937cde45e3a591fb3b9484ffdcaddbdfa144 with its submodules.
# <packet>: this directory. Prior reviewers' scripts are read from the evidence commit
# 1f33e530291358c047cf5eea7229ca9ef5399944 (review-evidence/665s6-r1/reviews/*/scripts/).
set -u
C=$1; P=$2; R=$P/receipts; S=$P/scratch; E=1f33e530291358c047cf5eea7229ca9ef5399944
source "$P/scripts/env.sh"
mkdir -p "$R/gates" "$S/probes/r791" "$S/probes/r792" "$S/oldtap" "$S/drop" "$S/rmut" "$S/bnd"
for f in cdc_plants.py ctrl_boundary_probe.py ctrl_split_drop_probe.cpp split_reviewer_mutants.py soc_vs_tb_wiring.py; do
  git -C "$C" show "$E:review-evidence/665s6-r1/reviews/R791-1/scripts/$f" > "$S/probes/r791/$f"; done
git -C "$C" show "$E:review-evidence/665s6-r1/reviews/R792-1/scripts/cdc_check_probes.py" > "$S/probes/r792/cdc_check_probes.py"
cd "$C" || exit 2
# 1. the CDC check: its self-test, this round's allowance probes, both round 1 reviewers' probes
(cd tb/verilator/milan_dp && python3 -I split_cdc_check.py --selftest) > "$R/split-cdc-selftest.log" 2>&1 &
python3 -I "$P/scripts/cdc_allowance_probes.py" . > "$R/cdc-allowance-probes.log" 2>&1 &
python3 -I "$S/probes/r791/cdc_plants.py" . > "$R/r791-cdc-plants.log" 2>&1 &
python3 -I "$S/probes/r792/cdc_check_probes.py" . > "$R/r792-1-cdc-check-probes.log" 2>&1 &
# 2. the split leg at the head
(make -C tb/verilator/milan_dp -j16 build-split SPLIT_MDIR="$S/obj_split_head" && \
 cd tb/verilator/milan_dp && "$S/obj_split_head/Vmilan_dp_split") > "$S/split-leg-raw.log" 2>&1 &
wait
# 3. mutants, the leg on round 1's tap, and R791's probes
git show 6584b7bf:hdl/milan/KL_ctrl_split.sv > "$S/oldtap/KL_ctrl_split.sv"
make -C tb/verilator/milan_dp split-mutants > "$R/split-mutants.log" 2>&1 &
(make -s -C tb/verilator/milan_dp build-split SPLIT_MDIR="$S/obj_split_oldtap" CTLS_SRC="$S/oldtap/KL_ctrl_split.sv" && \
 cd tb/verilator/milan_dp && "$S/obj_split_oldtap/Vmilan_dp_split") > "$S/split-leg-old-tap-raw.log" 2>&1 &
python3 -I "$S/probes/r791/split_reviewer_mutants.py" . "$S/rmut" --jobs 8 > "$R/r791-split-reviewer-mutants.log" 2>&1 &
(cd "$S/drop" && verilator --cc --exe --build -j 4 --top-module KL_ctrl_split -Wno-fatal "$C/hdl/milan/KL_ctrl_split.sv" \
   "$C/third_party/verilog-axis/rtl/axis_fifo.v" "$S/probes/r791/ctrl_split_drop_probe.cpp" > build.log 2>&1 && \
 ./obj_dir/VKL_ctrl_split) > "$R/r791-drop-probe.log" 2>&1 &
python3 -I "$S/probes/r791/ctrl_boundary_probe.py" . "$S/bnd" > "$R/r791-ctrl-boundary-probe.log" 2>&1 &
wait
# 4. static wiring and names
python3 -I "$S/probes/r791/soc_vs_tb_wiring.py" . > "$R/r791-soc-vs-tb-wiring.log" 2>&1
python3 -I "$P/scripts/split_port_names.py" . > "$R/split-port-names.log" 2>&1
# 5. the docs-gates-0 gates round 1 left red, and the naming ratchet (the em dash gate needs the pinned renderer venv)
for g in "measure_naming.py --check" check_port_contracts.py check_py_idiom.py "measure_test_evidence.py --check" check_doc_style.py; do
  n=${g%% *}; python3 scripts/$g > "$R/gates/${n%.py}.log" 2>&1; echo $? > "$R/gates/${n%.py}.rc"; done
"$TOOLS/md-venv-40cdefe08ebd/bin/python3" scripts/check_em_dash.py --base a9d69c774dee18b90eead74c9f2dda24cf8fdeb8 > "$R/gates/check_em_dash.log" 2>&1
# 6. restore: remove the build outputs the runs left in the clone, then verify the exact head
#    (git status --porcelain --ignored empty; git diff-index HEAD empty; write-tree == HEAD^{tree}; gitlinks)
