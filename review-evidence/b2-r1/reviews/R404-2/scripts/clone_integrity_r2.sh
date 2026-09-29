#!/usr/bin/env bash
# Prove the review clone is at the exact head, byte for byte. Usage: clone_integrity_r2.sh <clone>
set -u; cd "$1" || exit 2
H=d76763733e088cd21bbdd587927c8cf2f26cc8b3; B=13eda870d1a6cf3f946fc228a98862366b08d102; R1=c37f1d04e39be0344dfde77e793cdfa441bd4869
echo "HEAD $(git rev-parse HEAD) expected $H"
echo "tree $(git rev-parse HEAD^{tree}) expected 2e2dcd08dd16575aee614c8ff694a2c6c964b95c"
echo "parent $(git rev-parse HEAD^) expected $R1; grandparent $(git rev-parse HEAD^^) expected $B"
echo "status --porcelain --ignored=no lines: $(git status --porcelain | wc -l)"
git diff --quiet HEAD && echo "worktree == HEAD: yes" || echo "worktree == HEAD: NO"
git diff --cached --quiet HEAD && echo "index == HEAD: yes" || echo "index == HEAD: NO"
echo "index entries with assume-unchanged/skip-worktree flags: $(git ls-files -v | grep -vc '^H ')"
diff <(git ls-files -s | awk '{print $1" "$2" "$4}') <(git ls-tree -r HEAD | awk '{print $1" "$3" "$4}') > /dev/null && echo "index records (mode, blob, path) == HEAD tree: yes" || echo "index records == HEAD tree: NO"
echo "diff --raw base..head:"; git diff --raw $B $H
echo "diff --raw round1..head:"; git diff --raw $R1 $H
for f in $(git diff --name-only $B $H); do
  echo "$f worktree-blob $(git hash-object "$f") tree-blob $(git rev-parse HEAD:"$f") mode $(git ls-tree HEAD "$f" | cut -d' ' -f1) filemode $(stat -c %a "$f")"; done
echo "gitlinks at head vs base:"
for g in external gptp-processor protocol-processor third_party/verilog-axis; do
  echo "  $g head $(git rev-parse HEAD:$g) base $(git rev-parse $B:$g)"; done
git submodule status
