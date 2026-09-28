#!/bin/sh
# Compare FASTCONNECT section 16 checkbox states and the D3 section 15.1
# decision register between two commits. Run from the parent repository root.
# Usage: sh checkbox_register_compare.sh <old> <new>
set -u
OLD=$1; NEW=$2
FC=docs/design/SAVED_STATE_FASTCONNECT.md
D3=docs/design/SAVED_STATE_MATERIALIZATION.md
for c in c07232228c12b72805dd20e6852bf93f25794da0 "$OLD" "$NEW"; do
  git show "$c:$FC" | awk '/^## 16\. /{f=1} f' > /tmp/r380_2_fc16_$$.txt
  printf '%s checked=%s unchecked=%s\n' "$c" \
    "$(grep -c '^- \[x\]' /tmp/r380_2_fc16_$$.txt)" "$(grep -c '^- \[ \]' /tmp/r380_2_fc16_$$.txt)"
  grep -n -E '^- \[[ x]\]' /tmp/r380_2_fc16_$$.txt | sed -E 's/^([0-9]+):(- \[[ x]\]).{0,60}.*/\2/' | tr -d '\n'; echo
done
rm -f /tmp/r380_2_fc16_$$.txt
echo "## checkbox state sequence identical old->new:"
a=$(git show "$OLD:$FC" | awk '/^## 16\. /{f=1} f' | grep -o -E '^- \[[ x]\]' | tr -d '\n')
b=$(git show "$NEW:$FC" | awk '/^## 16\. /{f=1} f' | grep -o -E '^- \[[ x]\]' | tr -d '\n')
[ "$a" = "$b" ] && echo SAME || echo DIFFERENT
echo "## D3 15.1 register rows byte-identical old->new:"
ra=$(git show "$OLD:$D3" | grep -E '^\| DR[0-9]' | sha256sum)
rb=$(git show "$NEW:$D3" | grep -E '^\| DR[0-9]' | sha256sum)
echo "old $ra"; echo "new $rb"; [ "$ra" = "$rb" ] && echo SAME || echo DIFFERENT
echo "## ruled rows count at new:"; git show "$NEW:$D3" | grep -c -E '^\| DR[0-9][a-z]?: .*\*\*RULED\*\*'
echo "## whole 15.1 section identical old->new:"
sa=$(git show "$OLD:$D3" | awk '/^### 15\.1/{f=1;next} f&&/^### 15\.2/{exit} f' | sha256sum)
sb=$(git show "$NEW:$D3" | awk '/^### 15\.1/{f=1;next} f&&/^### 15\.2/{exit} f' | sha256sum)
[ "$sa" = "$sb" ] && echo SAME || echo DIFFERENT
echo "## files changed old->new:"; git diff --name-status "$OLD" "$NEW"
echo "## gitlinks old vs new:"; git ls-tree -r "$OLD" | awk '$2=="commit"'; git ls-tree -r "$NEW" | awk '$2=="commit"'
