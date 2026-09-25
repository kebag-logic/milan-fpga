#!/bin/sh
# Focused static/doc gates at the reviewed head (read-only --check modes).
# usage: static_gates.sh <clone>  ; writes receipts/static/<gate>.log and summary.txt
set -u
CLONE=$1
PACKET=${PACKET:-$REVIEWS/551-r297-2-packet}
R=$PACKET/receipts/static; mkdir -p "$R"; : > "$R/summary.txt"
BASE=864b36f5e9450ef64f75ca3f0d68c44330e447d7
cd "$CLONE" || exit 2
run() { name=$1; shift; "$@" > "$R/$name.log" 2>&1; echo "$name rc=$?" | tee -a "$R/summary.txt"; }
run docs_check python3 scripts/docs_check.py
run em_dash python3 scripts/check_em_dash.py --base "$BASE"
run doc_style python3 scripts/check_doc_style.py
run gen_toc python3 scripts/gen_toc.py --check
run doc_paths python3 scripts/check_doc_paths.py
run module_matrix python3 docs/traceability/gen_module_matrix.py --check
run py_idiom python3 scripts/check_py_idiom.py
run cpp_idiom python3 scripts/check_cpp_idiom.py
run sv_idiom python3 scripts/check_sv_idiom.py
run rtl_source_lists python3 scripts/check_rtl_source_lists.py
run pp_srcs python3 scripts/pp_srcs.py --check
run diff_check git diff --check "$BASE" HEAD
PATH=$(dirname "$VERILATOR"):$PATH run lint_rtl python3 scripts/lint_rtl.py --check
