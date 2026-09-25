#!/usr/bin/env bash
# R306-3 delta verification for PR #560 at 9d66cfe0. Read-only against the clone.
# Usage: verify_delta.sh <clone> <python-with-cmarkgfm-html5lib-pyyaml> <scratch-dir>
set -u
CLONE=$1; PY=$2; SCR=$3
HEAD=9d66cfe0dc87ffe4a5f45691d5c86b041b050b38
PREV=224ec0e9a9fa129924bf8f0433cf70b4140f7bd2
PIN=990f96526bb89356c963a260ebbdcf2a77e6623a
cd "$CLONE" || exit 2
echo "== delta scope"; git diff --numstat "$PREV" "$HEAD"; git diff --raw "$PREV" "$HEAD"
echo "== gsi_mutants MUTATIONS length"
python3 -I -c "import ast;t=ast.parse(open('tb/verilator/milan_dp/gsi_mutants.py').read());print([len(n.value.elts) for n in t.body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='MUTATIONS'])"
echo "== anchors and figure ids at the pin"
git -C protocol-processor show "$PIN:docs/architecture/06_aecp_engine.md" | grep -n 'id="fig-06-lineage"'
git -C protocol-processor show "$PIN:docs/architecture/05_acmp_engine.md" | grep -n 'id="fig-05-settled"'
echo "== docs_check in git archives (no submodule content)"
for rev in "$HEAD" "$PREV"; do
  d="$SCR/archive_$rev"; rm -rf "$d"; mkdir -p "$d"
  git archive --format=tar "$rev" | tar -x -C "$d"
  (cd "$d" && python3 -I scripts/docs_check.py > "$SCR/archive.log" 2>&1; rc=$?; tail -3 "$SCR/archive.log"; echo "rc=$rc rev=$rev")
done
echo "== in-clone gates"
for g in "scripts/docs_check.py" "scripts/gen_toc.py --verify-anchors" "scripts/gen_toc.py --check" \
         "scripts/check_doc_paths.py" "scripts/check_em_dash.py --base c266432d" \
         "scripts/measure_test_evidence.py --check" "scripts/measure_test_evidence.py --selftest" \
         "scripts/check_py_idiom.py" "scripts/check_py_idiom.py --selftest"; do
  # shellcheck disable=SC2086
  "$PY" -I $g > "$SCR/gate.log" 2>&1; rc=$?; echo "rc=$rc $g :: $(grep -v '^\s*$' "$SCR/gate.log" | tail -1)"
done
git diff --check "$PREV" "$HEAD"; echo "diff --check rc=$?"
rm -rf scripts/__pycache__
