#!/usr/bin/env bash
# Focused static gates at the head under review. Read-only on the clone;
# integrity is re-verified by verify_head.py afterwards.
#   run_gates.sh CLONE OUTDIR BASE
set -u
clone="$1"; out="$2"; base="$3"
mkdir -p "$out"
: > "$out/SUMMARY.txt"
run() {
  local name="$1"; shift
  local began=$SECONDS
  (cd "$clone" && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE "$@") > "$out/$name.out" 2>&1
  local rc=$?
  printf '%s rc=%s secs=%s  :: %s\n' "$name" "$rc" "$((SECONDS - began))" "$*" >> "$out/SUMMARY.txt"
}
run py_idiom            python3 scripts/check_py_idiom.py
run py_idiom_selftest   python3 scripts/check_py_idiom.py --selftest
run sh_idiom            python3 scripts/check_sh_idiom.py
run sh_idiom_selftest   python3 scripts/check_sh_idiom.py --selftest
run fail_fast           python3 scripts/measure_fail_fast.py --check
run test_evidence       python3 scripts/measure_test_evidence.py --check
run test_evidence_selftest python3 scripts/measure_test_evidence.py --selftest
run docs_check          python3 scripts/docs_check.py
run em_dash             python3 scripts/check_em_dash.py --base "$base"
run em_dash_selftest    python3 scripts/check_em_dash.py --selftest
run doc_style           python3 scripts/check_doc_style.py
run doc_paths           python3 scripts/check_doc_paths.py
run toc_check           python3 scripts/gen_toc.py --check
run toc_anchors         python3 scripts/gen_toc.py --verify-anchors
run baremetal_check     python3 scripts/check_baremetal_only.py --check
run baremetal_selftest  python3 scripts/check_baremetal_only.py --selftest
run ci_scope_selftest   python3 scripts/ci_scope.py --selftest
run py_compile          python3 -c "import ast,sys; ast.parse(open('scripts/test_suite_cancellation.py').read()); print('parsed')"
run bash_n              bash -n scripts/run_all_suites.sh
cat "$out/SUMMARY.txt"
