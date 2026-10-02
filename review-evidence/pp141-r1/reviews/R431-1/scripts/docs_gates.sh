#!/bin/bash
# Docs and generator-consistency gates over an exported tree; each gate's own
# exit status is recorded. Usage: docs_gates.sh TREE REPO
T="$1"; R="$2"; cd "$T" || exit 2
all=0
for c in "make check" "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" \
         "python3 scripts/check-integrator-params.py" "python3 scripts/render-wavedrom.py --check" \
         "make stale" "python3 scripts/gen_matrix.py --check" "python3 scripts/check_upc_map.py" \
         "python3 scripts/check_m9_opcodes.py"; do
  echo "=== $c"; out=$($c 2>&1); rc=$?; printf '%s\n' "$out" | tail -6; echo "rc=$rc"
  [ $rc -eq 0 ] || all=1
done
echo "=== git diff --check 03c842a7 4a40b179"
git -C "$R" diff --check 03c842a780064048b0a1a3de29214174a1c13934 4a40b1798e463d09aafd74632408003229bcc673; rc=$?
echo "rc=$rc"; [ $rc -eq 0 ] || all=1
echo "ALL rc=$all"; exit $all
