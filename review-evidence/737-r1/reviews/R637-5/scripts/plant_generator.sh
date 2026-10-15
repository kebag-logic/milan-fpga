#!/usr/bin/env bash
# Plant worker-count mismatches in a disposable copy of the head tree and
# record whether scripts/ci_gate_workflows.py --check refuses each one.
# Usage: plant_generator.sh <repo-clone> <scratch-dir>
set -u
repo=$1; scratch=$2
tpl=.github/ci-templates/rtl.yml
run() {  # name, sed-expression-or-command
  name=$1; shift
  d="$scratch/plant-$name"; rm -rf "$d"; mkdir -p "$d"
  git -C "$repo" archive HEAD | tar -x -C "$d"
  ( cd "$d" && eval "$*" )
  before=$(sha256sum "$d/$tpl" "$d/.github/workflows/rtl.yml" | sha256sum | cut -c1-16)
  out=$(cd "$d" && python3 scripts/ci_gate_workflows.py --check 2>&1); rc=$?
  echo "=== $name rc=$rc treehash=$before"
  printf '%s\n' "$out" | tail -2
}
run baseline true
run arm_4_total_6 "sed -i 's/            5) test \"\$(cat/            4) test \"\$(cat/' $tpl && grep -c '4) test' $tpl"
run expect_5_total_6 "sed -i 's/--require-target-sha --expect 6 /--require-target-sha --expect 5 /' $tpl && grep -c 'expect 5 ' $tpl"
run total_7_arm_5 "sed -i 's/        shard: \[0, 1, 2, 3, 4, 5\]/        shard: [0, 1, 2, 3, 4, 5, 6]/; s/        total: \[6\]/        total: [7]/' $tpl && grep -c 'total: \[7\]' $tpl"
run arm_duplicated "sed -i 's/^\(            5) test .*milan_dp ;;\)$/\1\n\1/' $tpl && grep -c '5) test' $tpl"
run expect_duplicated "sed -i 's/--require-target-sha --expect 6 /--require-target-sha --expect 6 --expect 6 /' $tpl && grep -c 'expect 6 --expect 6' $tpl"
run template_edit_not_regenerated "sed -i '0,/fail-fast: true/s//fail-fast: false/' $tpl && grep -c 'fail-fast: false' $tpl"
run generated_hand_edit "sed -i '0,/timeout-minutes: 5/s//timeout-minutes: 6/' .github/workflows/rtl.yml && grep -c 'timeout-minutes: 6' .github/workflows/rtl.yml"
