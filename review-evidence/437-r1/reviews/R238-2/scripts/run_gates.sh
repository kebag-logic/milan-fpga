#!/usr/bin/env bash
# Focused gate bank for R238-2 at the exact head. Usage: run_gates.sh <clone> <receipt-dir>
set -u
clone=$1; out=$2
export TMPDIR=${TMPDIR:-/tmp}
cd "$clone" || exit 2
run() {
  name=$1; shift
  "$@" >"$out/$name.log" 2>&1
  echo "$? $name :: $*" | tee -a "$out/exits.txt"
}
: >"$out/exits.txt"
git rev-parse HEAD HEAD^{tree} >"$out/head.txt"
run toc_selftest python3 -B scripts/gen_toc.py --selftest
run toc_check python3 -B scripts/gen_toc.py --check
run toc_anchors python3 -B scripts/gen_toc.py --verify-anchors
run toc_sites python3 -B scripts/gen_toc.py --sites
run emdash_selftest python3 -B scripts/check_em_dash.py --selftest
run emdash_base_574 python3 -B scripts/check_em_dash.py --base 574c29fa111c74e5e5ed63e4670aff1f492e28e2
run emdash_base_88e python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896
run docs_check python3 -B scripts/docs_check.py
run docs_check_selftest python3 -B scripts/docs_check.py --selftest
run doc_style python3 -B scripts/check_doc_style.py
run doc_style_selftest python3 -B scripts/check_doc_style.py --selftest
run doc_paths python3 -B scripts/check_doc_paths.py
run py_idiom python3 -B scripts/check_py_idiom.py
run py_idiom_selftest python3 -B scripts/check_py_idiom.py --selftest
run hygiene python3 -B scripts/check_hygiene.py --check
run hygiene_selftest python3 -B scripts/check_hygiene.py --selftest
run test_evidence python3 -B scripts/measure_test_evidence.py --check
run fail_fast python3 -B scripts/measure_fail_fast.py --check
run cohesion_selftest python3 -B scripts/measure_cohesion.py --selftest
run control_flow_selftest python3 -B scripts/measure_control_flow.py --selftest
run todo_ownership python3 -B scripts/check_todo_ownership.py
run diff_check git diff --check 574c29fa111c74e5e5ed63e4670aff1f492e28e2 HEAD
git status --porcelain=v1 --ignored >"$out/status_after.txt"
