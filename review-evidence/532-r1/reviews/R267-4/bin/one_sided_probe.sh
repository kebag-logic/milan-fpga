#!/usr/bin/env bash
# one_sided_probe.sh: inside sandbox.sh, with head.sh and proof_one_case.py in
# the cwd, grade each of the proof's four one-sided overlap cases ALONE against
# the head proof and against the one overlap-conjunct mutant it is meant to
# kill, with the parallel start order natural, forced A-first and forced
# B-first. The head must pass every case in every order; each mutant must fail
# its own case in every order, so its kill depends on no other case and on no
# start order. Prints one line per (order, case, proof).
set -uo pipefail
a_first=('  replay parallel-b "$pr_b" "$worktree_b" "$slot_b" &' '  sleep 1; replay parallel-b "$pr_b" "$worktree_b" "$slot_b" &')
b_first=('  replay parallel-a "$pr_a" "$worktree_a" "$slot_a" &' '  { sleep 1; replay parallel-a "$pr_a" "$worktree_a" "$slot_a"; } &')
declare -A case_of=(
  [Q25]='run A is refused after taking slot A, before run B takes slot B|a-refused-first|23|1|FAIL overlap'
  [Q26]='run B is refused after taking slot B, before run A takes slot A|b-refused-first|23|1|FAIL overlap'
  [Q27]='run B dies before taking slot B while run A holds slot A|b-never-holds|23|1|FAIL overlap'
  [Q28]='run A dies before taking slot A while run B holds slot B|a-never-holds|23|1|FAIL overlap'
)
declare -A mutant=(
  [Q25]='    && ! ended parallel-a && ! ended parallel-b; then|    && ! ended parallel-b; then'
  [Q26]='    && ! ended parallel-a && ! ended parallel-b; then|    && ! ended parallel-a; then'
  [Q27]='  if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \|  if await_holder parallel-a "$slot_a" \'
  [Q28]='  if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \|  if await_holder parallel-b "$slot_b" \'
)
for order in natural A-first B-first; do
  for m in Q25 Q26 Q27 Q28; do
    for proof in head "$m"; do
      subs=()
      if [ "$order" = A-first ]; then subs=("${a_first[@]}"); fi
      if [ "$order" = B-first ]; then subs=("${b_first[@]}"); fi
      if [ "$proof" != head ]; then subs+=("${mutant[$m]%%|*}" "${mutant[$m]#*|}"); fi
      out=$(python3 proof_one_case.py head.sh "/tmp/$order-$m-$proof" "${case_of[$m]}" "${subs[@]}")
      result=$(printf '%s\n' "$out" | grep -m1 -E '^  (ok  |FAIL) ')
      overlap=$(printf '%s\n' "$out" | grep -m1 -E '^(PASS|FAIL) overlap' | cut -c1-40)
      if [ "$proof" = head ]; then
        verdict=$([ "${result:2:2}" = ok ] && echo "HEAD-PASSES-CASE" || echo "HEAD-FAILS-CASE")
      else
        verdict=$([ "${result:2:2}" = ok ] && echo "MUTANT-SURVIVES" || echo "MUTANT-KILLED")
      fi
      printf '%-8s %-4s %-5s %-17s | %s\n' "$order" "$m" "$proof" "$verdict" "$overlap"
    done
  done
done
