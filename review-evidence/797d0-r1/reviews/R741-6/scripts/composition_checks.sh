#!/usr/bin/env bash
# Reproduce the composition checks of this review on a clean checkout.
# Usage: composition_checks.sh <repo-at-candidate> <out-dir> [python-with-pinned-renderer]
# The third argument is a Python that has tools/markdown/requirements.txt
# installed (gen_toc.py and check_em_dash.py refuse to judge without it).
set -u
REPO=$1; OUT=$2; PYR=${3:-python3}
CAND=297b642f06aede7b818a5451722c75032fb05099
HEAD_SRC=e8ec8d209a3d9055cc034a23d94925a0bf7b9a63
DEV=e61a4afaa54a598ceec08b7b5879285256cc60b6
OLDBASE=1f29f189279f9fc0132f4918e47342b87d22f33a
mkdir -p "$OUT"; cd "$REPO" || exit 2
export PYTHONDONTWRITEBYTECODE=1
[ "$(git rev-parse HEAD)" = "$CAND" ] || { echo "not at candidate"; exit 2; }

# Structure: candidate tree equals the PR head tree; dev sync reproduces.
{
  echo "candidate tree $(git rev-parse $CAND^{tree}) head tree $(git rev-parse $HEAD_SRC^{tree})"
  echo "automerge $(git merge-tree --write-tree 8d8c2e366a2d49506b91a195de0094a440e7bc39 $DEV) recorded $(git rev-parse b48b2fd5a^{tree})"
  echo "PR files also changed by dev since $OLDBASE:"
  git diff --name-only $OLDBASE $DEV -- $(git diff --name-only $DEV $CAND)
} > "$OUT/structure.txt" 2>&1

run() { n=$1; shift; ( "$@" > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc" ) & }
run inv_check python3 scripts/docs_inventory.py --check
run inv_selftest python3 scripts/docs_inventory.py --selftest
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run gate_wf python3 scripts/ci_gate_workflows.py --check
run doc_paths python3 scripts/check_doc_paths.py
run doc_style python3 scripts/check_doc_style.py
run docs_check "$PYR" scripts/docs_check.py
run toc_check "$PYR" scripts/gen_toc.py --check
run toc_anchors "$PYR" scripts/gen_toc.py --verify-anchors
run toc_selftest "$PYR" scripts/gen_toc.py --selftest
run em_dash "$PYR" scripts/check_em_dash.py --base $DEV
run diffcheck git diff --check $DEV $CAND
wait
for f in "$OUT"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
