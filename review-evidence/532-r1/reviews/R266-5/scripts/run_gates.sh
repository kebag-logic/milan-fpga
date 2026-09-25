#!/usr/bin/env bash
# Run the composition-relevant documentation/contract gates on a checkout.
# Usage: run_gates.sh <checkout> <receipt-dir> <python> [base-sha]
set -u
repo=$1; out=$2; py=$3; base=${4:-7ddbbdc9be73728b239718c8976261c7e0ad0563}
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
cat > "$out/gates.list" <<LIST
docs_check|scripts/docs_check.py
em_dash_base|scripts/check_em_dash.py --base $base
doc_style|scripts/check_doc_style.py
doc_style_selftest|scripts/check_doc_style.py --selftest
doc_map_check|docs/DOC_MAP.gen.py --check
baremetal_check|scripts/check_baremetal_only.py --check
baremetal_selftest|scripts/check_baremetal_only.py --selftest
naming_check|scripts/measure_naming.py --check
fail_fast_check|scripts/measure_fail_fast.py --check
todo_ownership|scripts/check_todo_ownership.py
test_evidence_check|scripts/measure_test_evidence.py --check
test_evidence_selftest|scripts/measure_test_evidence.py --selftest
hygiene_check|scripts/check_hygiene.py --check
py_idiom|scripts/check_py_idiom.py
sh_idiom|scripts/check_sh_idiom.py
ci_events_check|scripts/ci_events.py --check
ci_events_selftest|scripts/ci_events.py --selftest
doc_paths|scripts/check_doc_paths.py
archive|scripts/check_archive.py
toc_selftest|scripts/gen_toc.py --selftest
toc_anchors|scripts/gen_toc.py --verify-anchors
toc_check|scripts/gen_toc.py --check
control_flow_selftest|scripts/measure_control_flow.py --selftest
ci_scope_selftest|scripts/ci_scope.py --selftest
LIST
run_one() {
  name=${1%%|*}; cmd=${1#*|}
  ( cd "$repo" && timeout 3000 $py $cmd ) > "$out/$name.log" 2>&1
  echo "$name rc=$? :: $cmd" > "$out/$name.rc"
}
export -f run_one; export repo out py
tr '\n' '\0' < "$out/gates.list" | xargs -0 -P 8 -I{} bash -c 'run_one "$@"' _ {}
cat "$out"/*.rc | sort > "$out/SUMMARY.txt"
cat "$out/SUMMARY.txt"
