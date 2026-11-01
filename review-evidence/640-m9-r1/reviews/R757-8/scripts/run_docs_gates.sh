#!/bin/sh
# Re-run the docs gates that read the changed pages, on a disposable archive-plus-git copy.
# Usage: run_docs_gates.sh <clone> <scratch dir> <receipts dir>
set -u
SRC=$1; S=$2; OUT=$3
rm -rf "$S/gatecopy"; git clone -q --no-hardlinks "$SRC" "$S/gatecopy" || exit 9
cd "$S/gatecopy" || exit 9
git fetch -q origin 1f29f189279f9fc0132f4918e47342b87d22f33a 2>/dev/null
rc() { n=$1; shift; "$@" >"$OUT/gate_$n.log" 2>&1; echo "$n rc=$?" >>"$OUT/gates_summary.txt"; }
: >"$OUT/gates_summary.txt"
rc docs_check python3 -I scripts/docs_check.py
rc doc_style python3 -I scripts/check_doc_style.py
rc em_dash python3 -I scripts/check_em_dash.py --base 1f29f189279f9fc0132f4918e47342b87d22f33a
rc doc_paths python3 -I scripts/check_doc_paths.py
rc toc_check python3 -I scripts/gen_toc.py --check
rc toc_anchors python3 -I scripts/gen_toc.py --verify-anchors
rc diff_check git diff --check 1f29f189279f9fc0132f4918e47342b87d22f33a HEAD
