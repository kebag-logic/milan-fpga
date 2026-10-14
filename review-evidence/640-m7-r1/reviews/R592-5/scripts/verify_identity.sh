#!/usr/bin/env bash
# Usage: verify_identity.sh <clone>. Proves the review clone holds exact head bytes.
set -u; cd "$1" || exit 2
H=4c5d70b50230fbd5da347852d39daf7f23b3df0b T=8156e281ac181efc76139470e3cf5c530ae17793
rc=0
[ "$(git rev-parse HEAD)" = $H ] && echo "HEAD ok $H" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = $T ] && echo "tree ok $T" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = $T ] && echo "index tree ok" || { echo "INDEX MISMATCH"; rc=1; }
git diff --quiet HEAD -- && echo "worktree vs HEAD clean (content+mode)" || { echo DIRTY; rc=1; }
u=$(git status --porcelain --ignore-submodules=none --untracked-files=all | wc -l); echo "porcelain lines: $u"; [ "$u" = 0 ] || rc=1
# raw bytes: rehash every tracked regular file and compare with the index blob
bad=$(git ls-files -s | awk '$1!="160000"{print $2" "$4}' | while read -r b f; do [ "$(git hash-object --no-filters -- "$f")" = "$b" ] || echo "$f"; done | wc -l)
echo "tracked blobs rehashed, mismatches: $bad"; [ "$bad" = 0 ] || rc=1
git ls-files -s | awk '$1=="160000"{print $2" "$4}' | while read -r g p; do
  if [ -e "$p/.git" ]; then a=$(git -C "$p" rev-parse HEAD); s=$([ "$a" = "$g" ] && echo ok || echo MISMATCH); echo "gitlink $p $g checkout $a $s"; else echo "gitlink $p $g (not initialized)"; fi
done
for p in gptp-processor protocol-processor third_party/verilog-axis third_party/tsn-c-stack third_party/lwSRP; do [ -z "$(git -C "$p" status --porcelain --untracked-files=all)" ] && echo "submodule $p clean" || { echo "submodule $p DIRTY"; rc=1; }; done
echo "rc=$rc"; exit $rc
