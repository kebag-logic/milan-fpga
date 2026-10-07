#!/bin/sh
# Usage: static_checks.sh <disposable-copy-of-the-head-tree> <receipt-dir>
# Record gates and generator re-runs at the head. Generators write into the
# copy; the final `git status` must be empty (records regenerate identically).
set -u
T=$1; R=$2; mkdir -p "$R"; cd "$T" || exit 99
export PYTHONHASHSEED=0
run() { n=$1; shift; "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc"; echo "$n rc=$(cat "$R/$n.rc")"; }
run port_contracts_check python3 scripts/check_port_contracts.py
run naming_check python3 scripts/measure_naming.py --check
run submodule_docs python3 scripts/check_submodule_docs.py
run diagram_pngs python3 scripts/check_diagram_pngs.py
run resource_gate_check python3 syn/ooc/pp_resource_gate.py check-baseline
run nvm_capture python3 scripts/check_nvm_capture.py
run pp_baseline_selftest python3 syn/ooc/pp_baseline.py --selftest
run pp_baseline_mutants python3 syn/ooc/pp_baseline_mutants.py
run pp_srcs_check python3 scripts/pp_srcs.py --check
run docs_check python3 scripts/docs_check.py
run doc_style python3 scripts/check_doc_style.py
run doc_paths python3 scripts/check_doc_paths.py
run port_contracts_write python3 scripts/check_port_contracts.py --write-budget
run naming_write python3 scripts/measure_naming.py --write-budget
run boundaries_gen python3 docs/diagrams/submodule_boundaries.gen.py
git status --porcelain=v1 > "$R/regen_status.txt"
echo "tracked changes after regeneration: $(wc -l < "$R/regen_status.txt")"
