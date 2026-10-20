#!/usr/bin/env bash
# usage: parent_gates.sh <record-dir>   the parent consumer gates on the scratch parent, unpiped
S=<scratch>; P="$S/parent"; rec="$1"; mkdir -p "$rec"
G="$S/scripts/gate.sh"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$S/tmpdir" VERILATOR_JOBS=2
test "$(git -C "$P" rev-parse --show-toplevel)" = "$P" || exit 3
git -C "$P" rev-parse HEAD > "$rec/parent-HEAD.txt"
git -C "$P" log --format='%h %s' -5 > "$rec/parent-log.txt"
git -C "$P" ls-files -s protocol-processor > "$rec/gitlink.txt"
git -C "$P/protocol-processor" rev-parse HEAD > "$rec/submodule-HEAD.txt"
git -C "$P" submodule status > "$rec/submodule-status.txt"
git -C "$P" status --short > "$rec/parent-status-before.txt"
"$G" "$rec" g01_cpp_idiom "$P" python3 scripts/check_cpp_idiom.py
"$G" "$rec" g02_py_idiom "$P" python3 scripts/check_py_idiom.py
"$G" "$rec" g03_rtl_source_lists "$P" python3 scripts/check_rtl_source_lists.py
"$G" "$rec" g04_pp_srcs "$P" python3 scripts/pp_srcs.py --check --selftest
"$G" "$rec" g05_port_contracts "$P" python3 scripts/check_port_contracts.py
"$G" "$rec" g06_naming "$P" python3 scripts/measure_naming.py --check
"$G" "$rec" g07_test_evidence "$P" python3 scripts/measure_test_evidence.py --check
"$G" "$rec" g08_docs_check "$P" python3 scripts/docs_check.py
"$G" "$rec" g09_sh_idiom "$P" python3 scripts/check_sh_idiom.py
"$G" "$rec" g11_lint_rtl "$P" python3 scripts/lint_rtl.py --check
"$G" "$rec" g12_pp_shadow "$P" make -j8 -O -C tb/verilator/pp_shadow
"$G" "$rec" g13_nvm_cosim_lint "$P" make -j8 -O -C tb/verilator/nvm_cosim lint
"$G" "$rec" g14_nvm_cosim_quick "$P" make -j8 -O -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2
"$G" "$rec" g16_milan_dp_render "$P" make -j8 -O -C tb/verilator/milan_dp_render
"$G" "$rec" g15_milan_dp "$P" make -j8 -O -C tb/verilator/milan_dp SIM_JOBS=2
"$G" "$rec" g10_test_builder "$P" python3 sw/builder/test_builder.py
"$G" "$rec" g17_xvlog "$P" flock <vivado-lock> python3 scripts/xvlog_gate.py --check
git -C "$P" status --short > "$rec/parent-status-after.txt"
git -C "$P/protocol-processor" status --short --ignored > "$rec/submodule-status-after.txt"
echo ALL-DONE > "$rec/parent.done"
