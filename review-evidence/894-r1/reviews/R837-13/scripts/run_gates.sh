#!/bin/sh
# Run the documentation, idiom and grader gates concurrently on a clean clone.
# Usage: run_gates.sh <clean-clone> <log-dir>
set -u
C=$1; L=$2; mkdir -p "$L"
cd "$C" || exit 2
B=66f713267f201d1a00d7f711e04b3a996d804dee
run() { n=$1; shift; ( "$@" > "$L/$n.log" 2>&1; echo $? > "$L/$n.rc" ) & }
run docs_check python3 -I -B scripts/docs_check.py
#run em_dash_base python3 -I -B scripts/check_em_dash.py --base $B
#run em_dash_867 python3 -I -B scripts/check_em_dash.py --base 867faf1e7321e1260f86701f01d7de0c94e67490
#run em_dash_4ae python3 -I -B scripts/check_em_dash.py --base 4ae887a1
run doc_style python3 -I -B scripts/check_doc_style.py
run gptp_docs python3 -I -B scripts/check_gptp_docs.py
run doc_map python3 -I -B docs/DOC_MAP.gen.py --check
run cpp_idiom python3 -I -B scripts/check_cpp_idiom.py
run py_idiom python3 -I -B scripts/check_py_idiom.py
run diff_check git diff --check $B HEAD
run solution_docs python3 -I -B scripts/check_solution_docs.py
run submodule_docs python3 -I -B scripts/check_submodule_docs.py
run feature_status python3 -I -B scripts/check_feature_status.py
run todo_ownership python3 -I -B scripts/check_todo_ownership.py
run hygiene python3 -I -B scripts/check_hygiene.py --check
run doc_paths python3 -I -B scripts/check_doc_paths.py
run archive python3 -I -B scripts/check_archive.py
T=tb/verilator/ctrl_service_budget
run flip_both python3 -I -B $T/flip_grade.py --check
run flip_1x1 python3 -I -B $T/flip_grade.py --check --point 1x1/1if
run flip_8x8 python3 -I -B $T/flip_grade.py --check --point 8x8/2if
run flip_selftest python3 -I -B $T/flip_grade.py --selftest
run load_check python3 -I -B $T/load_grade.py --check
run load_selftest python3 -I -B $T/load_grade.py --selftest
run rows_tiers_selftest python3 -I -B $T/rows_tiers.py --selftest
wait
git status --porcelain > "$L/after_status.txt"; echo "after: $(wc -l < "$L/after_status.txt") changed paths"
for f in "$L"/*.rc; do n=$(basename "$f" .rc); printf '%s: rc %s :: %s\n' "$n" "$(cat "$f")" "$(tail -n 1 "$L/$n.log")"; done
