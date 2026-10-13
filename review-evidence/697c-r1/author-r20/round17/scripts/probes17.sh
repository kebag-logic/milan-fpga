#!/usr/bin/env bash
# Scratch (round 17): the earlier reviewers' probes, unchanged, on one disposable clone, with the Git PATH names:
# R584-14's two spelling probes, R585-14's five probe scripts and R584-12's store_probe.py.
# usage: probes17.sh <clone> <work dir> <log prefix>
set -u
clone=$1; work=$2; out=$3
r584=$VALIDATION_STORAGE/697c-a583/round17/r584-14
r585=$VALIDATION_STORAGE/697c-a583/round16/r585-14/probes
store=$VALIDATION_STORAGE/697c-a583/round15/probes/R584-12/scripts/store_probe.py
export PYTHONDONTWRITEBYTECODE=1
rm -rf "$work"; mkdir -p "$work"
echo "git: $(command -v git) $(git --version)"
python3 -I -B "$r584/superproject_spelling_probe.py" "$clone" "$work/sp" > "$out-r584_14_superproject_spelling.txt" 2>&1
echo "rc=$? r584_14 superproject_spelling_probe.py"
python3 -I -B "$r584/stack_spelling_probe.py" "$clone" "$work/st" > "$out-r584_14_stack_spelling.txt" 2>&1
echo "rc=$? r584_14 stack_spelling_probe.py"
for s in r585_14_superproject r585_14_superproject_sparse r585_14_superproject_sparse_gitlink \
         r585_14_superproject_sparse_gitlink_serve r585_14_probes; do
  bash "$r585/$s.sh" "$clone" "$work/$s" > "$out-$s.txt" 2>&1
  echo "rc=$? $s.sh"
done
python3 -I -B "$store" "$clone/sw/firmware/ctrl/test" "$clone/third_party/tsn-c-stack" "$work/store" > "$out-store_probe.txt" 2>&1
echo "rc=$? store_probe.py"
