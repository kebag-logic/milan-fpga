#!/bin/sh
# Usage: run_gates.sh <clean clone at exact head> <receipt dir>
# Runs the parser and engine suites, both mutation arms and the docs gate
# concurrently with pinned Verilator 5.050 first on PATH.
set -u
T=$1; R=$2; mkdir -p "$R"
PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH; export PATH
verilator --version > "$R/verilator_version.txt"
job() { n=$1; d=$2; shift 2; ( cd "$T/$d" && "$@" ) > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc"; }
job parser_run tb/verilator/parser make run VERILATOR=verilator &
job parser_mutants tb/verilator/parser python3 mutants.py &
job engine_run tb/verilator/engine make run VERILATOR=verilator &
job engine_mutants tb/verilator/engine python3 mutants.py &
job docs_gate . python3 scripts/check_docs.py &
job docs_selftest_I . python3 -I scripts/check_docs.py --selftest &
job docs_selftest . python3 scripts/check_docs.py --selftest &
job diff_check . git diff --check 3e3a4e7695ce66eed609089f280c2fba45b24d36 762fbd6716b50337e7644a4918c216b3143aeb5b &
wait
echo done > "$R/ALL_DONE"
