#!/bin/sh
# Reviewer-owned residual-claim search at a commit (tracked files only, gitlinks excluded).
# usage: claim_search.sh <repo> <commit>
cd "$1" || exit 2
git grep -n -I -i -E 'sr_admitted|raw (admission )?verdict|admission verdict|slope mux|cbs slope|bw-gate|bw_gate|bandwidth gate|unbudgeted|budgets? (the|every|for)|shaper (keeps|reads|takes|budgets)|stream gate' "$2" -- \
  ':!protocol-processor' ':!gptp-processor' ':!external' ':!*.png' ':!*.svg'
