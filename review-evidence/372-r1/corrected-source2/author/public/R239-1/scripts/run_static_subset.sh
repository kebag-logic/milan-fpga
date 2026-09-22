#!/bin/sh
# R239: an independent subset of the docs-workflow gates most relevant to the
# changed files, run exactly as .github/workflows/docs.yml invokes them, in a
# scratch git clone of the review clone checked out at the exact head.
# Not the full 45-command manager bank; each exit is recorded.
set -u
G=$VALIDATION_STORAGE/r239-372-r1-work/gitclone
OUT=$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r1-r239/raw/static
BASE=52711029f374650dc93830d5ea28e81cb5c8f410
mkdir -p "$OUT"
: > "$OUT/summary.txt"
cd "$G" || exit 2
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) base $BASE" >> "$OUT/summary.txt"
run() { # name, command...
  name=$1; shift
  PYTHONDONTWRITEBYTECODE=1 "$@" > "$OUT/$name.log" 2>&1
  echo "$name exit=$? :: $*" >> "$OUT/summary.txt"
}
run docs_check python3 scripts/docs_check.py
run em_dash python3 scripts/check_em_dash.py --base "$BASE"
run doc_style python3 scripts/check_doc_style.py
run doc_paths python3 scripts/check_doc_paths.py
run gen_toc_anchors python3 scripts/gen_toc.py --verify-anchors
run gen_toc_check python3 scripts/gen_toc.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run sv_idiom python3 scripts/check_sv_idiom.py
run cpp_idiom python3 scripts/check_cpp_idiom.py
run py_idiom python3 scripts/check_py_idiom.py
run hygiene python3 scripts/check_hygiene.py --check
cat "$OUT/summary.txt"
