#!/usr/bin/env bash
# [R238] reproduce every measurement of this report, in order.
#
# Prerequisites (read-only on the review checkout):
#   scratch/clone-head  = git clone --no-hardlinks <review checkout>, detached at
#                         65df1df50a80cd5f540a93d8f0cfabc97da3da75, with the three
#                         required submodules populated at their pins from the
#                         review checkout's local copies (no network)
#   scratch/clone-base  = worktree of clone-head at 88e9276b2a220c716f64a843f7e1eb8f9265e896,
#                         submodules populated the same way
#   scratch/issue437-comments.json = gh issue view 437 --json comments
# Renderer answers are cached in receipts/renderer-cache.json with every exact
# request and response; with the cache present no request leaves this host.
# Each step's exit code is appended to receipts/reproduce-exits.txt.
set -u
here=$(realpath "$(dirname "$0")/..")
cd "$here" || exit 2
: > receipts/reproduce-exits.txt
step() {
  local name=$1
  shift
  "$@" > "receipts/reproduce-$name.log" 2>&1
  printf '%-22s exit %d\n' "$name" "$?" >> receipts/reproduce-exits.txt
}
step integrity-pre   python3 -B scripts/integrity.py $VALIDATION_STORAGE/reviews/r238-437-r1 reproduce-pre
step gates-head      bash scripts/run_gates.sh scratch/clone-head head
step gates-base      bash scripts/run_gates.sh scratch/clone-base base
step probes          python3 -B scripts/probe_render.py
step e2e             python3 -B scripts/e2e_gate.py
step e2e-family-two  python3 -B scripts/e2e_family_two.py
step arms-vs-github  python3 -B scripts/arms_vs_github.py
step author-receipt  python3 -B scripts/author_receipt_check.py
step corpus          python3 -B scripts/corpus_compare.py
step census          python3 -B scripts/census.py
step prior-arms      python3 -B scripts/prior_arms.py
step mutants         python3 -B scripts/mutate.py
step candidate       python3 -B scripts/candidate_repair.py
step sweep           python3 -B scripts/sweep.py
step unfixed-f1      python3 -B scripts/unfixed_family_one.py
step navigation      python3 -B scripts/navigation_consumer.py
step integrity-post  python3 -B scripts/integrity.py $VALIDATION_STORAGE/reviews/r238-437-r1 reproduce-post
cat receipts/reproduce-exits.txt
