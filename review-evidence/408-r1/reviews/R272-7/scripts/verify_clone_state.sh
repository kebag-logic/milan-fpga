#!/usr/bin/env bash
# Verify a review clone is byte-exact at an expected head after probes:
# HEAD and tree, index == HEAD tree (blob ids and modes), no worktree or
# untracked change, and each required submodule gitlink checked out at the
# recorded commit.  Usage: verify_clone_state.sh <clone> <head> <tree>
set -u
clone=$1 head=$2 tree=$3
cd "$clone" || exit 2
fail=0
check() { if [ "$2" = "$3" ]; then echo "OK   $1 $2"; else echo "FAIL $1 got=$2 want=$3"; fail=1; fi; }
check HEAD "$(git rev-parse HEAD)" "$head"
check tree "$(git rev-parse 'HEAD^{tree}')" "$tree"
check index-tree "$(git write-tree)" "$tree"
git diff --quiet HEAD -- && echo "OK   worktree == HEAD (tracked bytes and modes)" || { echo "FAIL worktree differs"; fail=1; }
untracked=$(git ls-files --others --exclude-standard | wc -l)
check untracked-files "$untracked" 0
ignored=$(git status --porcelain --ignored | grep -c '^!!')
echo "INFO ignored entries: $ignored"
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
    want=$(git ls-tree HEAD "$sub" | awk '{print $3}')
    got=$(git -C "$sub" rev-parse HEAD 2>/dev/null || echo absent)
    check "gitlink:$sub" "$got" "$want"
    dirty=$(git -C "$sub" status --porcelain 2>/dev/null | wc -l)
    check "clean:$sub" "$dirty" 0
done
exit $fail
