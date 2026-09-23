#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Live proof for parallel act replay slots (#532). Run it with an AUDITED
# runner install, never with a candidate worktree's own copy of the runner:
# see "Parallel replay slots" in docs/testing/CI_WORKFLOWS.md.
#
# In order, it proves:
#   1. per-slot interruption cleanup: --interrupt-selftest in slot A;
#   2. the serial references: PR A, then PR B, one after the other in the
#      serial slot (default 0, today's replay);
#   3. isolation: PR A in slot A and PR B in slot B at the same time, each
#      with the verdict of its serial reference;
#   4. the collision control: PR A and PR B at the same time in ONE slot.
#      The second must be refused while the first holds the slot, and the
#      first must still reach its serial verdict. With --collide-default the
#      same control also runs on slot 0, which has no slot isolation at all.
#
# Exit 0 only when every proof holds. Each run's log, exit status and
# extracted verdict land in --logs, with a summary in --logs/SUMMARY.
set -euo pipefail

usage() {
  cat <<'EOF'
usage: act_slot_proof.sh --runner ABS --sha256 HEX --act-bin ABS --logs DIR
         --pr-a N --worktree-a DIR --pr-b N --worktree-b DIR
         [--slot-a N] [--slot-root-a DIR] [--slot-b N] [--slot-root-b DIR]
         [--serial-slot N] [--repo OWNER/REPO] [--workflow NAME]...
         [--collide-default]
EOF
}

runner="" sha="" act_bin="" logs="" repo="kebag-logic/milan-fpga"
pr_a="" worktree_a="" pr_b="" worktree_b=""
slot_a=1 slot_b=2 serial_slot=0 collide_default=0
slot_root_a=/var/lib/milan-act-ci slot_root_b=/var/lib/milan-act-ci
workflow_args=()

parse_arguments() {
  while [ "$#" -gt 0 ]; do
    if [ "$1" != --collide-default ] && [ "$#" -lt 2 ]; then usage >&2; exit 2; fi
    case "$1" in
      --runner) runner=$2 ;;
      --sha256) sha=$2 ;;
      --act-bin) act_bin=$2 ;;
      --logs) logs=$2 ;;
      --repo) repo=$2 ;;
      --pr-a) pr_a=$2 ;;
      --worktree-a) worktree_a=$2 ;;
      --pr-b) pr_b=$2 ;;
      --worktree-b) worktree_b=$2 ;;
      --slot-a) slot_a=$2 ;;
      --slot-b) slot_b=$2 ;;
      --slot-root-a) slot_root_a=$2 ;;
      --slot-root-b) slot_root_b=$2 ;;
      --serial-slot) serial_slot=$2 ;;
      --workflow) workflow_args+=(--workflow "$2") ;;
      --collide-default) collide_default=1; shift; continue ;;
      *) usage >&2; exit 2 ;;
    esac
    shift 2
  done
  for required in "$runner" "$sha" "$act_bin" "$logs" "$pr_a" "$worktree_a" \
    "$pr_b" "$worktree_b"; do
    if [ -z "$required" ]; then usage >&2; exit 2; fi
  done
  if [ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ]; then
    echo "slot A must be an isolated slot distinct from slot B" >&2
    exit 2
  fi
}

verify_runner() {
  local actual
  actual=$(sha256sum "$runner" | cut -d' ' -f1)
  if [ "$actual" != "$sha" ] || [ -w "$runner" ]; then
    echo "runner $runner is not the audited read-only install $sha" >&2
    exit 2
  fi
  mkdir -p "$logs"
  if [ -n "$(ls -A "$logs")" ]; then
    echo "log directory $logs is not empty" >&2
    exit 2
  fi
}

# slot_root SLOT: the slot root the command line gave that slot.
slot_root() {
  if [ "$1" -eq "$slot_a" ]; then echo "$slot_root_a"; else echo "$slot_root_b"; fi
}

# replay LABEL PR WORKTREE SLOT: one PR run; its log, status and verdict.
replay() {
  local label=$1 pr=$2 worktree=$3 slot=$4 status
  local -a slot_args=()
  if [ "$slot" -ne 0 ]; then slot_args=(--slot "$slot" --slot-root "$(slot_root "$slot")"); fi
  if (cd "$worktree" && python3 -I "$runner" --pr "$pr" --repo "$repo" \
    --worktree "$worktree" --trusted-install-sha256 "$sha" --act-bin "$act_bin" \
    --sudo "${workflow_args[@]}" "${slot_args[@]}") >"$logs/$label.log" 2>&1; then
    status=0
  else
    status=$?
  fi
  printf '%s\n' "$status" >"$logs/$label.status"
  {
    printf 'exit %s\n' "$status"
    sed -n -E 's/^act-ci: ([a-z-]+): (PASS|FAILED).*/\1 \2/p' "$logs/$label.log"
  } >"$logs/$label.verdict"
}

# same_verdict LABEL REFERENCE: whether two runs reached identical verdicts.
same_verdict() {
  cmp -s "$logs/$1.verdict" "$logs/$2.verdict"
}

# compare LABEL REFERENCE: record whether LABEL kept REFERENCE's verdict.
compare() {
  if same_verdict "$1" "$2"; then record PASS "$1 = $2"; else record FAIL "$1 != $2"; fi
}

record() {
  printf '%s %s\n' "$1" "$2" | tee -a "$logs/SUMMARY"
}

# await_holder LABEL SLOT: block until run LABEL holds SLOT, or fail.
await_holder() {
  local label=$1 slot=$2 marker="act-ci: running " polls=0
  if [ "$slot" -ne 0 ]; then marker="act-ci: slot $slot: own daemon"; fi
  while [ "$polls" -lt 720 ]; do
    if grep -q -F "$marker" "$logs/$label.log" 2>/dev/null; then return 0; fi
    sleep 5
    polls=$((polls + 1))
  done
  return 1
}

# collide SLOT REFUSAL: A holds SLOT, B arrives and must be refused.
collide() {
  local slot=$1 refusal=$2 holder rival_status
  replay "collide-$slot-holder" "$pr_a" "$worktree_a" "$slot" &
  holder=$!
  if ! await_holder "collide-$slot-holder" "$slot"; then
    wait "$holder"
    record FAIL "collision slot $slot: the holder never held the slot"
    return
  fi
  replay "collide-$slot-rival" "$pr_b" "$worktree_b" "$slot"
  wait "$holder"
  rival_status=$(cat "$logs/collide-$slot-rival.status")
  if [ "$rival_status" = 2 ] \
    && grep -q -E "$refusal" "$logs/collide-$slot-rival.log" \
    && same_verdict "collide-$slot-holder" serial-a; then
    record PASS "collision slot $slot: the rival was refused and the holder kept its serial verdict"
  else
    record FAIL "collision slot $slot: see collide-$slot-*.log"
  fi
}

main() {
  parse_arguments "$@"
  verify_runner
  if (cd "$logs" && python3 -I "$runner" --interrupt-selftest --act-bin "$act_bin" \
    --sudo --slot "$slot_a" --slot-root "$slot_root_a") >"$logs/interrupt-$slot_a.log" 2>&1; then
    record PASS "interrupt self-test in slot $slot_a"
  else
    record FAIL "interrupt self-test in slot $slot_a"
  fi
  replay serial-a "$pr_a" "$worktree_a" "$serial_slot"
  replay serial-b "$pr_b" "$worktree_b" "$serial_slot"
  replay parallel-a "$pr_a" "$worktree_a" "$slot_a" &
  local parallel_a=$!
  replay parallel-b "$pr_b" "$worktree_b" "$slot_b" &
  wait "$parallel_a" "$!"
  compare parallel-a serial-a
  compare parallel-b serial-b
  collide "$slot_a" "is in use by another runner invocation"
  if [ "$collide_default" -eq 1 ]; then collide 0 "act-toolcache|already exist"; fi
  if grep -q '^FAIL' "$logs/SUMMARY"; then exit 1; fi
  record PROVED "every slot proof held"
}

main "$@"
