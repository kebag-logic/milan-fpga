#!/usr/bin/env bash
# R410-3 composition check: is d5f73bac..4e558491 this lane's reviewed content
# (b2db3a97..616cbdf1) plus the stated renames? Replays the lane diff on main
# in a disposable clone and compares each file against the head, then prints
# the hunk-level (-U0, line numbers stripped) difference per file.
#   composition.sh HEAD_REPO SCRATCH
set -uo pipefail
repo=$1; scratch=$2
BASE=b2db3a970cedbbff2f8ba813acb96122c442bc58 R2=616cbdf1e54a56420e35b53cd161116702f7172d
MAIN=d5f73bac158276a9fcf549185bad5c65c0498dae HEAD_=4e558491c608dc88efc7963a77cb6b49bce2a46e
rm -rf "$scratch/replay"; git clone -q --no-checkout "$repo" "$scratch/replay"; cd "$scratch/replay" || exit 2
echo "merge 5609f8f parents: $(git rev-parse 5609f8f^1) $(git rev-parse 5609f8f^2)"
echo "merge-base(R2, MAIN) = $(git merge-base $R2 $MAIN)"
echo "== files: lane (BASE..R2) vs merged (MAIN..HEAD) numstat"
diff <(git diff --numstat $BASE $R2) <(git diff --numstat $MAIN $HEAD_)
echo "== MAIN..HEAD -- hdl: $(git diff --name-only $MAIN $HEAD_ -- hdl | wc -l) files"
echo "== paths outside the lane's 11 files and tb/maap/README.md touched by MAIN..HEAD:"
git diff --name-only $MAIN $HEAD_ | grep -vxF -f <(git diff --name-only $BASE $R2; echo tb/maap/README.md) || echo "  none"
git checkout -q --detach $MAIN
git diff $BASE $R2 | git apply -3 >/dev/null 2>&1
echo "== lane diff replayed on MAIN (git apply -3), file vs HEAD:"
for f in $(git diff --name-only $BASE $R2) tb/maap/README.md; do
  if git diff --quiet $HEAD_ -- "$f"; then echo "  SAME $f"; else echo "  DIFF $f"; fi
done
echo "== hunk-level difference, lane (BASE..R2) vs merged (MAIN..HEAD), per DIFF file:"
for f in tb/pp_top/README.md tb/pp_top/sim_main.cpp tb/rx_validator/README.md tb/rx_validator/sim_main.cpp tb/pp_top/acmp_mutants.py tb/maap/README.md; do
  echo "##### $f"
  diff <(git diff -U0 $BASE $R2 -- "$f" | grep '^[+-]' | grep -v '^+++\|^---') \
       <(git diff -U0 $MAIN $HEAD_ -- "$f" | grep '^[+-]' | grep -v '^+++\|^---')
done
echo "== 4e55849 alone:"; git show --stat --format='%H %s' 4e55849 | cat
git diff 5609f8f 4e55849 | cat
