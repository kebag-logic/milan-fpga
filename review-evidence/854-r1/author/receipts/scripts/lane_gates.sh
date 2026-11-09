#!/usr/bin/env bash
# lane_gates.sh <head>: the gates this change touches, one log and one rc per gate, never piped, on the clean clone
# of the head. The sweep is separate (native-shards or serial run_all_suites.sh); docs.yml is docsyml_all.sh.
set -u
H=$1; S=$VALIDATION_STORAGE/scratch/854-a756; W=$S/gclone; G=$S/gates/lane
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$G"
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
test -z "$(git status --porcelain)" || exit 5
source "$here/env.sh"
export MAKEFLAGS="-j8 --no-print-directory" CI_CAMPAIGN_JOBS=8 HOME=$S/home-gates
mkdir -p "$HOME"
BASEP=$PATH
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
P=$BASEP
run diffcheck "git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD"
run docs_inventory "python3 scripts/docs_inventory.py --check"
run measure_test_evidence "python3 scripts/measure_test_evidence.py --check"
run lint_rtl "python3 scripts/lint_rtl.py --check --self-test --jobs 8"
run pp_srcs "python3 scripts/pp_srcs.py --check --selftest"
run yosys_elaborate "syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow"
run ooc_selftests "set -e; python3 syn/ooc/dp_srcs.py --selftest; python3 syn/ooc/ooc_tcl_selftest.py; python3 syn/ooc/pp_baseline.py --selftest; python3 syn/ooc/pp_baseline_mutants.py; python3 syn/ooc/pp_baseline_reports_selftest.py; python3 syn/ooc/pp_resource_gate.py --selftest; python3 syn/ooc/pp_resource_gate_mutants.py; python3 syn/ooc/pp_resource_gate.py check-baseline; python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null; python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null"
run drops_mutant "make -C tb/verilator/pp_shadow drops-mutant"
run fw_selftest "python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8"
run fw_coverage "set -e; python3 sw/firmware/gtest/fw_coverage.py --selftest; python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8"
run test_builder "python3 sw/builder/test_builder.py --require-rv32"
P=$S/venv-behave/bin:$BASEP
run behave "cd tests && behave --no-capture -f plain"
git status --short --ignored > "$G/tree-after.txt"
echo done > "$G/DONE"
