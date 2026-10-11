#!/usr/bin/env bash
# Focused documentation gates for the files PR #718 touches, at the exact head checkout.
P=${R597_PACKET:-$(cd "$(dirname "$0")/.." && pwd)}; out=$P/receipts/docs; mkdir -p $out; : > $out/summary.tsv
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$P/scratch/tmp
PY=${PY:-python3}
cd "${CHECKOUT:?set CHECKOUT to the exact-head checkout}"
i=0
while IFS= read -r cmd; do
  i=$((i+1)); n=$(printf '%02d' $i)
  bash -c "$PY $cmd" > $out/$n.log 2>&1; rc=$?
  printf '%s\t%s\t%s\n' "$n" "$rc" "$cmd" >> $out/summary.tsv
done <<LIST
docs/diagrams/submodule_boundaries.gen.py --check
docs/diagrams/submodule_boundaries.gen.py --selftest
scripts/check_submodule_docs.py
scripts/check_submodule_docs.py --selftest
scripts/check_diagram_pngs.py
scripts/check_em_dash.py --base e8454e2751d05b02ee8e5a571857589ab358ab86
scripts/docs_check.py
scripts/check_doc_style.py
scripts/check_doc_paths.py
scripts/gen_toc.py --check
scripts/gen_toc.py --verify-anchors
docs/DOC_MAP.gen.py --check
scripts/check_cpp_idiom.py
scripts/check_py_idiom.py
scripts/check_hygiene.py --check
scripts/check_nvm_capture.py
scripts/measure_test_evidence.py --check
LIST
