#!/bin/bash
# Two docs PRs that each lengthen a different page, on a disposable clone: does the audit page conflict?
# Usage: merge_sim.sh CLONE LABEL
set -u
cd "$1" || exit 2
label=$2
g() { git -c user.name=probe -c user.email=probe@example.invalid "$@"; }
start=$(git rev-parse HEAD)
git checkout -q -b sim-a "$start"
printf '\nAdded by branch A.\n' >> docs/guides/README.md
python3 -I scripts/docs_inventory.py --check >/dev/null; echo "$label branch A after its edit: --check rc=$?"
python3 -I scripts/docs_inventory.py --write >/dev/null
g add -A; g commit -q -m a
git checkout -q -b sim-b "$start"
printf '\nAdded by branch B.\n' >> docs/testing/CI_IMAGE.md
python3 -I scripts/docs_inventory.py --write >/dev/null
g add -A; g commit -q -m b
echo "$label audit page touched by branch A: $(git diff --name-only "$start" sim-a | grep -c DOCUMENTATION_AUDIT), by branch B: $(git diff --name-only "$start" sim-b | grep -c DOCUMENTATION_AUDIT)"
if g merge -q --no-edit sim-a >/dev/null 2>&1; then
  echo "$label merge: clean"; python3 -I scripts/docs_inventory.py --check >/dev/null; echo "$label merged --check rc=$?"
else
  echo "$label merge: CONFLICT in $(git diff --name-only --diff-filter=U | tr '\n' ' ')"; git merge --abort
fi
git checkout -q --detach "$start"; git branch -q -D sim-a sim-b
