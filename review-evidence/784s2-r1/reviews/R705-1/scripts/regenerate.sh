#!/usr/bin/env bash
# Regeneration receipts for #784 step 2.
# A: run the generator in write mode on a pristine scratch copy of the head; the copy must stay clean.
# B: export dev a8594bb9, substitute only the runs-on label in the four templates and the three
#    generators that write runs-on, regenerate, and compare the four workflows with the head's bytes.
# C: compare the head templates with that substituted dev export.
# Usage: regenerate.sh <reviewed-checkout> <pristine-scratch-copy> <scratch-dir> <python-bin-dir>
set -u
repo=$1 copy=$2 scratch=$3 bin=$4
export PATH="$bin:/usr/bin:/bin" PYTHONDONTWRITEBYTECODE=1
git=/usr/bin/git head=847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 dev=a8594bb95631fa5c49d18fa0bbc9530e31ad59aa
echo "## A. regenerate at head in a scratch copy"
(cd "$copy" && python3 scripts/ci_gate_workflows.py; echo "generator rc=$?"; echo "status lines after regeneration: $($git status --porcelain | wc -l)")
echo "## B. dev export, label-only substitution, regenerate"
d=$scratch/dev-regen
rm -rf "$d"; mkdir -p "$d"
$git -C "$repo" archive "$dev" | tar -x -C "$d"
sed -i 's/runs-on: ubuntu-latest/runs-on: ubuntu-24.04/' "$d"/.github/ci-templates/*.yml
sed -i 's/"runs-on": "ubuntu-latest"/"runs-on": "ubuntu-24.04"/' \
  "$d"/scripts/ci_gate_workflows.py "$d"/scripts/ci_runtime_workflows.py "$d"/scripts/ci_suite_workflows.py
(cd "$d" && python3 scripts/ci_gate_workflows.py --root "$d"; echo "dev-regen generator rc=$?")
for f in docs elaborate rtl-fast rtl; do
  if $git -C "$repo" show "$head:.github/workflows/$f.yml" | cmp -s - "$d/.github/workflows/$f.yml"; then
    echo "$f.yml: regenerated-from-dev bytes identical to head"
  else
    echo "$f.yml: DIFFERS from head"; $git -C "$repo" show "$head:.github/workflows/$f.yml" | diff - "$d/.github/workflows/$f.yml" | head -20
  fi
done
echo "## C. head templates vs label-substituted dev templates"
for f in docs elaborate rtl-fast rtl; do
  if $git -C "$repo" show "$head:.github/ci-templates/$f.yml" | cmp -s - "$d/.github/ci-templates/$f.yml"; then
    echo "$f template: identical"
  else
    echo "$f template differs (head < > substituted dev):"; $git -C "$repo" show "$head:.github/ci-templates/$f.yml" | diff - "$d/.github/ci-templates/$f.yml"
  fi
done
