#!/usr/bin/env bash
# overlap_order_probe.sh: inside sandbox.sh, grade the proof's `serialize` case
# (the parallel runs never overlap) against the head proof and the three
# overlap-conjunct mutants, with the parallel start order forced each way.
# Shows which conjunct the case exercises depends on which run wins the
# stand-in's queue lock. Needs head.sh and proof_one_case.py in the cwd.
set -uo pipefail
case_line="the parallel runs never overlap|serialize|23|1|FAIL overlap"
a_first=('  replay parallel-b "$pr_b" "$worktree_b" "$slot_b" &' '  sleep 1; replay parallel-b "$pr_b" "$worktree_b" "$slot_b" &')
b_first=('  replay parallel-a "$pr_a" "$worktree_a" "$slot_a" &' '  { sleep 1; replay parallel-a "$pr_a" "$worktree_a" "$slot_a"; } &')
declare -A mutant=(
  [head]=""
  [Q26]='    && ! ended parallel-a && ! ended parallel-b; then|    && ! ended parallel-a; then'
  [Q27]='  if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \|  if await_holder parallel-a "$slot_a" \'
  [Q28]='  if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \|  if await_holder parallel-b "$slot_b" \'
)
for order in A-first B-first; do
  for m in head Q26 Q27 Q28; do
    if [ "$order" = A-first ]; then subs=("${a_first[@]}"); else subs=("${b_first[@]}"); fi
    if [ -n "${mutant[$m]}" ]; then subs+=("${mutant[$m]%%|*}" "${mutant[$m]#*|}"); fi
    out=$(python3 proof_one_case.py head.sh "/tmp/$order-$m" "$case_line" "${subs[@]}")
    result=$(printf '%s\n' "$out" | grep -m1 -E '^  (ok  |FAIL) ')
    overlap=$(printf '%s\n' "$out" | grep -m1 -E '^(PASS|FAIL) overlap' | cut -c1-60)
    verdict=$([ "${result:2:2}" = ok ] && echo "case passes (mutant would SURVIVE)" || echo "case fails (mutant KILLED)")
    [ "$m" = head ] && verdict=$([ "${result:2:2}" = ok ] && echo "case passes (head correct)" || echo "case FAILS at head")
    printf '%-8s %-5s %-38s | %s\n' "$order" "$m" "$verdict" "$overlap"
  done
done
