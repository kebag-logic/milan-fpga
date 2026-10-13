#!/bin/sh
# run_gates.sh REPO OUTDIR : run the focused documentation/style/source gates
# named by the PR's validation list, one log + rc per gate, then a summary.
REPO=$1; OUT=$2
mkdir -p "$OUT"
cd "$REPO" || exit 2
export PYTHONDONTWRITEBYTECODE=1
run() {
  name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1
  rc=$?
  printf '%s\trc=%s\t%s\n' "$name" "$rc" "$*" | tee -a "$OUT/SUMMARY.tsv"
}
: > "$OUT/SUMMARY.tsv"
run measure_naming python3 scripts/measure_naming.py --check
run measure_test_evidence python3 scripts/measure_test_evidence.py --check
run check_py_idiom python3 scripts/check_py_idiom.py
run check_cpp_idiom python3 scripts/check_cpp_idiom.py
run docs_check python3 scripts/docs_check.py
run check_doc_style python3 scripts/check_doc_style.py
run gen_toc python3 scripts/gen_toc.py --check
run check_em_dash python3 scripts/check_em_dash.py --base c6bd08c6
run check_doc_paths python3 scripts/check_doc_paths.py
run check_nvm_capture python3 scripts/check_nvm_capture.py
run check_soc_sources python3 scripts/check_soc_sources.py
run check_rtl_source_lists python3 scripts/check_rtl_source_lists.py
run check_rtl_source_lists_selftest python3 scripts/check_rtl_source_lists.py --selftest
run pp_srcs python3 scripts/pp_srcs.py --check --selftest
run diff_check git diff --check c6bd08c6 HEAD
