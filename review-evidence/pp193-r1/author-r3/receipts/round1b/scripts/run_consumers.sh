#!/usr/bin/env bash
# usage: run_consumers.sh <log dir> [gate ...]
# The scratch parent's consumer gates, in sequence; <name>.log/.rc/.sec each.
set -u
P=<scratch>/parent
out=$1; shift
mkdir -p "$out"
. <scratch>/scripts/env-parent.sh
cd "$P" || exit 2
[ "$(git rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C protocol-processor rev-parse --show-toplevel)" = "$P/protocol-processor" ] || exit 3
{
  echo "parent HEAD $(git rev-parse HEAD)"
  git log --oneline -5
  echo "gitlink $(git ls-files -s protocol-processor)"
  echo "submodule HEAD $(git -C protocol-processor rev-parse HEAD)"
  git submodule status
  echo "working-tree diff sha256 $(git diff | sha256sum | cut -d' ' -f1)"
  git status --short
  verilator --version; sv2v --version; yosys -V | cut -c1-40; behave --version
} > "$out/STATE.txt" 2>&1
gate() {
  local name=$1; shift
  local t0=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
  echo $(( $(date +%s) - t0 )) > "$out/$name.sec"
}
all=(cpp_idiom py_idiom rtl_source_lists pp_srcs port_contracts measure_naming
     measure_test_evidence docs_check sh_idiom hygiene sv_idiom submodule_docs
     baremetal_only soc_sources todo_ownership lint_rtl bdd yosys_elaborate xvlog
     pp_shadow nvm_cosim_lint nvm_cosim_quick milan_dp_render milan_dp test_builder)
[ $# -gt 0 ] && all=("$@")
for g in "${all[@]}"; do
  case $g in
    cpp_idiom)             gate $g python3 scripts/check_cpp_idiom.py ;;
    py_idiom)              gate $g python3 scripts/check_py_idiom.py ;;
    rtl_source_lists)      gate $g python3 scripts/check_rtl_source_lists.py ;;
    pp_srcs)               gate $g python3 scripts/pp_srcs.py --check --selftest ;;
    port_contracts)        gate $g python3 scripts/check_port_contracts.py ;;
    measure_naming)        gate $g python3 scripts/measure_naming.py --check ;;
    measure_test_evidence) gate $g python3 scripts/measure_test_evidence.py --check ;;
    docs_check)            gate $g python3 scripts/docs_check.py ;;
    sh_idiom)              gate $g python3 scripts/check_sh_idiom.py ;;
    hygiene)               gate $g python3 scripts/check_hygiene.py --check ;;
    sv_idiom)              gate $g python3 scripts/check_sv_idiom.py ;;
    submodule_docs)        gate $g python3 scripts/check_submodule_docs.py ;;
    baremetal_only)        gate $g python3 scripts/check_baremetal_only.py --check ;;
    soc_sources)           gate $g python3 scripts/check_soc_sources.py ;;
    todo_ownership)        gate $g python3 scripts/check_todo_ownership.py ;;
    lint_rtl)              gate $g python3 scripts/lint_rtl.py --check --self-test --jobs 4 ;;
    bdd)                   gate $g bash -c 'cd tests && behave --no-capture -f plain' ;;
    yosys_elaborate)       gate $g syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow ;;
    test_builder)          gate $g python3 sw/builder/test_builder.py ;;
    xvlog)                 gate $g flock <tmp>/milan-vivado.lock python3 scripts/xvlog_gate.py --check ;;
    pp_shadow)             gate $g make -j8 -C tb/verilator/pp_shadow VERILATOR_JOBS=2 ;;
    nvm_cosim_lint)        gate $g make -j8 -C tb/verilator/nvm_cosim lint VERILATOR_JOBS=2 ;;
    nvm_cosim_quick)       gate $g make -j8 -C tb/verilator/nvm_cosim quick JOBS=2 POOL=2 VERILATOR_JOBS=2 ;;
    milan_dp_render)       gate $g make -j8 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2 ;;
    milan_dp)              gate $g make -j4 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2 ;;
    *) echo "unknown gate $g" > "$out/$g.log"; echo 2 > "$out/$g.rc" ;;
  esac
done
echo done > "$out/ALL.done"
