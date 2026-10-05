#!/bin/bash
# Mutation probe for the amended check_rtl_source_lists self-test arms (PR #663):
# each arm plants one defect in compare_tops in a disposable worktree and requires
# `check_rtl_source_lists.py --selftest` to exit nonzero; the control plants nothing.
# Usage: probe_tops.sh <clone> <scratch> <out>
clone=$1; scratch=$2; out=$3; mkdir -p "$out"
head=$(git -C "$clone" rev-parse HEAD)
declare -A ARM=(
  [control]=""
  [stale_never]='s/^    stale = sorted(n for n in recorded if n not in missing)$/    stale = []/'
  [unrecorded_never]='s/^    unrecorded = sorted(missing - set(recorded))$/    unrecorded = []/'
)
for arm in control stale_never unrecorded_never; do
  wt="$scratch/probe-tops-$arm"
  git -C "$clone" worktree add -q --detach "$wt" "$head"
  for sm in protocol-processor gptp-processor third_party/verilog-axis; do
    git -C "$clone/$sm" worktree add -q --detach "$wt/$sm" "$(git -C "$wt" rev-parse HEAD:$sm)"
  done
  if [ -n "${ARM[$arm]}" ]; then
    sed -i "${ARM[$arm]}" "$wt/scripts/check_rtl_source_lists.py"
    git -C "$wt" diff --stat -- scripts/check_rtl_source_lists.py | tail -1 > "$out/$arm.planted"
  fi
  (cd "$wt" && python3 scripts/check_rtl_source_lists.py --selftest > "$out/$arm.log" 2>&1); rc=$?
  echo "$arm rc $rc planted: $(cat "$out/$arm.planted" 2>/dev/null)"
  grep -E "FAIL\]" "$out/$arm.log" | head -4 | sed 's/^/    /'
  for sm in protocol-processor gptp-processor third_party/verilog-axis; do git -C "$clone/$sm" worktree remove --force "$wt/$sm"; done
  git -C "$clone" worktree remove --force "$wt"
done
