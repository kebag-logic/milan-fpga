#!/bin/sh
# Run the touched-scope documentation and code-quality gates concurrently.
# Usage: docs_gates.sh REPO OUTDIR
REPO=$1; OUT=$2; cd "$REPO" || exit 2
while read -r name cmd; do
  ( sh -c "$cmd" > "$OUT/gate_$name.log" 2>&1; echo $? > "$OUT/gate_$name.rc" ) &
done <<'LIST'
docs_check python3 -B scripts/docs_check.py
em_dash_r4 python3 -B scripts/check_em_dash.py --base c1049de1970e93d2c36ace62891ee9d947cd3191
em_dash_pr python3 -B scripts/check_em_dash.py --base db9aa8c9b135b34ff3d070a979dee70440b37cc6
doc_style python3 -B scripts/check_doc_style.py
doc_paths python3 -B scripts/check_doc_paths.py
gen_toc_check python3 -B scripts/gen_toc.py --check
gen_toc_anchors python3 -B scripts/gen_toc.py --verify-anchors
test_evidence python3 -B scripts/measure_test_evidence.py --check
hygiene python3 -B scripts/check_hygiene.py --check
cpp_idiom python3 -B scripts/check_cpp_idiom.py
py_idiom python3 -B scripts/check_py_idiom.py
naming python3 -B scripts/measure_naming.py --check
fail_fast python3 -B scripts/measure_fail_fast.py --check
todo python3 -B scripts/check_todo_ownership.py
control_flow_cohesion sh -c 'python3 -B scripts/measure_control_flow.py --check; a=$?; python3 -B scripts/measure_cohesion.py --check; b=$?; exit $((a|b))'
LIST
wait
for f in "$OUT"/gate_*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
