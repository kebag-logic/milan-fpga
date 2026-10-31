#!/usr/bin/env bash
# Reproduce the R731-3 delta checks for PR #822 at f7d5fc3c.
# Usage: r731_3_checks.sh <clone-with-submodules-at-head> <scratch-dir>
# The clone must be at f7d5fc3cc48ca80195428562fa86a46023df8e0d with its gitlinks
# checked out; it is restored with git checkout after each writing probe.
set -u
CLONE=$1; SCR=$2
HEAD=f7d5fc3cc48ca80195428562fa86a46023df8e0d
BASE=1e80128f0a467b58bf884b7d9bf62e013a2fb141
DEV=02ca829ad821f4233ab66f59978c65d3c3c9de70
PRIOR=4aa5666e730ae877766ed88c48bc8001e7a7b7b3
R4=5640e4d766c73adc330ee365848c250d8d67784e
R4B=3e67de9c1d42557f222edd2b079d23265bf1b726
PR826=4ee2aa9654196a00876dedade4b2e987c9c06e64
cd "$CLONE" || exit 2
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "not at head"; exit 2; }

echo "== round 4: automatic merge of the parents vs the recorded merge"
MT=$(git merge-tree --write-tree "$PRIOR" "$DEV" | head -1)
git merge-tree --write-tree --name-only "$PRIOR" "$DEV" | sed -n '2,/^$/p'
git diff --stat "$MT" "$R4"

echo "== round 4b: only the port census line changes"
git diff --stat "$R4" "$R4B"

echo "== round 5: patch-id and tree equality"
git diff "$BASE" "$PR826" | git patch-id --stable
git diff "$R4B" "$HEAD" | git patch-id --stable
echo "merge-tree $(git merge-tree --write-tree "$R4B" "$PR826") recorded $(git rev-parse "$HEAD^{tree}")"

echo "== git diff --check against dev"
git diff --check "$DEV" "$HEAD"; echo "rc=$?"

echo "== generators in the clone, restored after"
python3 -I scripts/check_port_contracts.py | tail -2
python3 -I scripts/check_port_contracts.py --write-budget >/dev/null
git diff --exit-code --stat scripts/port_docs.budget; echo "port budget diff rc=$?"
git checkout -- scripts/port_docs.budget
bash syn/yosys/ooc.sh --record-rom-digests >/dev/null
git diff --exit-code --stat syn/yosys/rom_digests.tsv; echo "rom ledger diff rc=$?"
git checkout -- syn/yosys/rom_digests.tsv
python3 -I scripts/check_submodule_docs.py; echo "rc=$?"
git status --porcelain

echo "== boundary diagram and CDC census in scratch clones"
mkdir -p "$SCR"
rm -rf "$SCR/gen"; git clone -q --no-checkout "$CLONE" "$SCR/gen"; git -C "$SCR/gen" checkout -q "$HEAD"
python3 -I "$SCR/gen/docs/diagrams/submodule_boundaries.gen.py" --check; echo "check rc=$?"
python3 -I "$SCR/gen/docs/diagrams/submodule_boundaries.gen.py"; echo "regen rc=$?"
git -C "$SCR/gen" status --porcelain
for c in "$BASE" "$DEV" "$PRIOR" "$HEAD" "$PR826"; do
  w="$SCR/cdc-$c"; rm -rf "$w" "$w.out"; mkdir -p "$w.out"
  git clone -q --no-checkout "$CLONE" "$w"; git -C "$w" checkout -q "$c"
  python3 -I "$w/docs/diagrams/cdc_census.gen.py" "$w.out/cdc_census" >/dev/null
  for e in svg drawio; do
    cmp -s "$w.out/cdc_census.$e" "$w/docs/diagrams/cdc_census.$e" && r=equal || r=DIFFERS
    echo "${c:0:8} cdc_census.$e $r"
  done
done
