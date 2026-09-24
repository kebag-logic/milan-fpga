#!/usr/bin/env bash
# unannounced_skew_probe.sh: inside sandbox.sh, with head.sh and proof_one_case.py
# in the cwd, grade the proof's "neither run reports its own slot daemon" case
# alone against the head and against mutant Q23 (await_holder accepts the generic
# running marker for a slot), with run B's start delayed by 0, 1 and 4 seconds.
# Its stand-in runs hold for the fixed FAKE_HOLD (3 s), so Q23 dies only while
# the two runs start within that hold of each other.
set -uo pipefail
case_line="neither run reports its own slot daemon|slot-unannounced|23|1|FAIL overlap"
q23=('  if [ "$slot" -ne 0 ]; then marker="act-ci: slot $slot: own daemon"; fi' '  :')
for delay in 0 1 4; do
  for proof in head Q23; do
    subs=('  replay parallel-b "$pr_b" "$worktree_b" "$slot_b" &' "  sleep $delay; replay parallel-b \"\$pr_b\" \"\$worktree_b\" \"\$slot_b\" &")
    if [ "$proof" = Q23 ]; then subs+=("${q23[@]}"); fi
    out=$(python3 proof_one_case.py head.sh "/tmp/skew-$delay-$proof" "$case_line" "${subs[@]}")
    result=$(printf '%s\n' "$out" | grep -m1 -E '^  (ok  |FAIL) ')
    overlap=$(printf '%s\n' "$out" | grep -m1 -E '^(PASS|FAIL) overlap' | cut -c1-40)
    printf 'B-delay=%ss %-4s case=%s | %s\n' "$delay" "$proof" "$([ "${result:2:2}" = ok ] && echo passes || echo fails)" "$overlap"
  done
done
