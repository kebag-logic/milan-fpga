#!/usr/bin/env bash
# Round R958-7 structural verification of the base-merge commit on PR #993.
# Usage: verify_base_merge.sh <superproject-clone> [--net]
# Read-only: uses git plumbing whose answer is an object ID, an integer or an
# exit status (rev-parse, rev-list --count, merge-base --is-ancestor,
# merge-tree --write-tree, ls-tree, diff --raw). Nothing is checked out,
# written to the index, or committed. --net adds two ls-remote reads.
set -u
REPO=${1:?superproject clone path}
NET=${2:-}
HEAD_SHA=25132e3029557d2d992dc42f2a77c6840e5c05d3
P1=a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35      # previously reviewed head
P2=0b5940237e8de8bd5912db87e5e036a78f59b5a6      # dev-soft-core tip (merge of PR #1015)
BASE=71bad8c0b973a15ee5f993a74f893ff7ff947c33    # dev-soft-core before PR #1015
PR1015=35d29eb71d2cc76717a4550787ef53ff2b72181f  # PR #1015 head
TREE=222e3e20fa0f6313632775aabf4f74a26c4417fc
SUB=third_party/tsn-c-stack
PIN977=5a07d9b7d87298f04b15aa28f0304ec88b0aef81
PIN1015=c3bff8f3dea03870ea7ae62965db360b509ee3b3
g() { git -C "$REPO" "$@"; }
fail=0
ok()  { printf 'PASS  %s\n' "$*"; }
bad() { printf 'FAIL  %s\n' "$*"; fail=1; }
eq()  { if [ "$2" = "$3" ]; then ok "$1: $2"; else bad "$1: got $2 want $3"; fi; }
anc() { if g merge-base --is-ancestor "$1" "$2"; then echo yes; else echo no; fi; }

echo "## git $(git --version)"
echo "## C1 parents"
eq "HEAD"            "$(g rev-parse HEAD)" "$HEAD_SHA"
eq "parent count"    "$(g rev-list --parents -n1 $HEAD_SHA | wc -w)" "3"
eq "parent 1"        "$(g rev-parse $HEAD_SHA^1)" "$P1"
eq "parent 2"        "$(g rev-parse $HEAD_SHA^2)" "$P2"
if [ "$NET" = "--net" ]; then
  eq "live origin dev-soft-core" "$(g ls-remote origin refs/heads/dev-soft-core | cut -f1)" "$P2"
  eq "live origin pull/993/head" "$(g ls-remote origin refs/pull/993/head | cut -f1)" "$HEAD_SHA"
fi

echo "## C2 tree"
eq "tree(HEAD)"      "$(g rev-parse $HEAD_SHA^{tree})" "$TREE"
eq "tree(parent 1)"  "$(g rev-parse $P1^{tree})" "$TREE"
eq "diff --raw P1..HEAD entries" "$(g diff --raw --no-renames $P1 $HEAD_SHA | wc -l)" "0"
eq "base is ancestor of HEAD (PR merges without a new tree)" "$(anc $P2 $HEAD_SHA)" "yes"

echo "## C3 gitlink"
gl() { g ls-tree "$1" $SUB | awk '{print $1" "$2" "$3}'; }
eq "gitlink(HEAD)"    "$(gl $HEAD_SHA)" "160000 commit $PIN977"
eq "gitlink(P1)"      "$(gl $P1)"       "160000 commit $PIN977"
eq "gitlink(P2)"      "$(gl $P2)"       "160000 commit $PIN1015"
eq "gitlink(PR1015)"  "$(gl $PR1015)"   "160000 commit $PIN1015"
if git -C "$REPO/$SUB" cat-file -e $PIN977^{commit} 2>/dev/null; then
  if git -C "$REPO/$SUB" merge-base --is-ancestor $PIN1015 $PIN977; then ok "submodule: $PIN1015 is an ancestor of $PIN977"; else bad "submodule: $PIN1015 not an ancestor of $PIN977"; fi
  echo "INFO  submodule commits in $PIN1015..$PIN977: $(git -C "$REPO/$SUB" rev-list --count $PIN1015..$PIN977)"
  if [ "$NET" = "--net" ]; then
    PUBMAIN=$(git ls-remote https://github.com/kebag-logic/tsn-c-stack.git refs/heads/main | cut -f1)
    echo "INFO  public tsn-c-stack main: $PUBMAIN"
    if git -C "$REPO/$SUB" cat-file -e "$PUBMAIN^{commit}" 2>/dev/null && git -C "$REPO/$SUB" merge-base --is-ancestor $PIN977 "$PUBMAIN"; then ok "submodule pin $PIN977 is reachable from public main"; else bad "submodule pin not shown reachable from public main"; fi
  fi
else
  bad "submodule objects absent; ancestry not checked"
fi
echo "INFO  all gitlinks at HEAD:"; g ls-tree -r $HEAD_SHA | awk '$2=="commit"{print "      "$3" "$4}'
echo "INFO  gitlinks differing P1..HEAD: $(g diff --raw $P1 $HEAD_SHA | grep -c ' 160000 ')"

echo "## C4 what the merge commit adds"
echo "INFO  merge bases of P1 and P2:"; g merge-base --all $P1 $P2 | sed 's/^/      /'
eq "dev-soft-core pre-#1015 tip is ancestor of P1" "$(anc $BASE $P1)" "yes"
eq "PR #1015 head is ancestor of P1"               "$(anc $PR1015 $P1)" "yes"
for m in 8d5737636c091eb086cdc141ad320c2ae93b59a6 aad9a6829830a43eb9c47a0f08fcf6929786e25f; do
  echo "INFO  branch merge $m parents: $(g rev-list --parents -n1 $m | cut -d' ' -f2-); ancestor of P1: $(anc $m $P1)"
done
eq "P2 parents" "$(g rev-list --parents -n1 $P2 | cut -d' ' -f2-)" "$BASE $PR1015"
eq "commits reachable from P2 and not from P1" "$(g rev-list --count $P2 ^$P1)" "1"
eq "commits reachable from HEAD and not from P1" "$(g rev-list --count $HEAD_SHA ^$P1)" "2"
eq "replayed merge BASE+PR1015 tree == tree(P2)" "$(g merge-tree --write-tree $BASE $PR1015 2>&1 | head -1)" "$(g rev-parse $P2^{tree})"
eq "replayed merge P1+P2 tree == tree(HEAD)"     "$(g merge-tree --write-tree $P1 $P2 2>&1 | head -1)" "$TREE"

echo "## C4 PR #1015 delta (BASE..P2) against HEAD, per path"
n=0; same=0; diffc=0
while IFS= read -r f; do
  n=$((n+1))
  a=$(g rev-parse -q --verify "$P2:$f" || echo absent)
  b=$(g rev-parse -q --verify "$HEAD_SHA:$f" || echo absent)
  c=$(g rev-parse -q --verify "$PR1015:$f" || echo absent)
  if [ "$a" = "$b" ]; then same=$((same+1)); st=IDENTICAL
  else diffc=$((diffc+1)); st="LATER-CHANGED-BY-$(g rev-list --count $PR1015..$P1 -- "$f")-COMMITS-ON-P1"; fi
  [ "$a" = "$c" ] || st="$st P2!=PR1015HEAD"
  printf '      %-52s %s\n' "$f" "$st"
done < <(g diff --name-only --no-renames $BASE $P2)
echo "INFO  #1015 paths: $n; byte-identical at HEAD to dev-soft-core tip: $same; carrying later P1-side commits: $diffc"
echo "INFO  paths differing HEAD vs dev-soft-core tip (the PR's net content): $(g diff --name-only --no-renames $P2 $HEAD_SHA | wc -l)"

echo "## commit message"
eq "message lines" "$(g log -1 --format=%B $HEAD_SHA | sed '/^$/d' | wc -l)" "1"
echo "INFO  subject: $(g log -1 --format=%s $HEAD_SHA)"

echo "## clone state"
eq "tracked changes (status --porcelain, submodules ignored=none)" "$(g status --porcelain --ignore-submodules=none | wc -l)" "0"
eq "index tree == HEAD tree" "$(g write-tree)" "$TREE"
echo "INFO  submodule status:"; g submodule status | sed 's/^/      /'
echo "## RESULT fail=$fail"
exit $fail
