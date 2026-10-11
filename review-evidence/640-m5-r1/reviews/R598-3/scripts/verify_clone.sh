#!/usr/bin/env bash
# Verify a review clone sits at the exact head with tracked bytes, modes, index
# and required submodule gitlinks intact. usage: verify_clone.sh <clone> <head> <tree>
set -u; c=$1; head=$2; tree=$3; rc=0
cd "$c" || exit 2
h=$(git rev-parse HEAD 2>/dev/null); t=$(git rev-parse HEAD^{tree} 2>/dev/null)
[ "$h" = "$head" ] && echo "head OK $h" || { echo "head MISMATCH $h"; rc=1; }
[ "$t" = "$tree" ] && echo "tree OK $t" || { echo "tree MISMATCH $t"; rc=1; }
it=$(git write-tree 2>/dev/null); [ "$it" = "$tree" ] && echo "index tree OK $it" || { echo "index tree MISMATCH $it"; rc=1; }
ns=$(git ls-files -s | awk '$3!=0' | wc -l); [ "$ns" = 0 ] && echo "index stages: all 0" || { echo "index: $ns non-zero stages"; rc=1; }
fl=$(git ls-files -v | grep -vc '^H '); [ "$fl" = 0 ] && echo "index flags: none hidden" || { echo "index: $fl entries with assume-unchanged/skip-worktree"; rc=1; }
git diff --quiet HEAD -- 2>/dev/null && echo "worktree bytes/modes: equal to HEAD" || { echo "worktree DIFFERS"; git diff --stat HEAD; rc=1; }
u=$(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l); [ "$u" = 0 ] && echo "status: clean, no untracked" || { echo "status:"; git status --porcelain --untracked-files=all; rc=1; }
ig=$(git status --porcelain --ignored --untracked-files=all | grep -c '^!!'); echo "ignored paths present: $ig"
git ls-files -s | awk '$1=="160000"{print "gitlink", $4, $2}'
git submodule status 2>&1 | sed 's/^/submodule-status: /'
for sm in gptp-processor protocol-processor third_party/verilog-axis; do
  want=$(git ls-files -s -- "$sm" | awk '{print $2}'); have=$(git -C "$sm" rev-parse HEAD 2>/dev/null)
  dirty=$(git -C "$sm" status --porcelain 2>/dev/null | wc -l)
  if [ "$want" = "$have" ] && [ "$dirty" = 0 ]; then echo "required submodule OK $sm $have clean"; else echo "required submodule BAD $sm want=$want have=$have dirty=$dirty"; rc=1; fi
done
[ $rc = 0 ] && echo "CLONE VERIFIED" || echo "CLONE NOT VERIFIED"
exit $rc
