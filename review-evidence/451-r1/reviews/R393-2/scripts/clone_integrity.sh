#!/bin/sh
# Verify a review clone is byte-exact at its expected head.
# Usage: clone_integrity.sh <clone> <expected-head>
set -u
C=$1; H=$2
cd "$C" || exit 2
T=$(mktemp)
echo "HEAD=$(git rev-parse HEAD) expected=$H tree=$(git rev-parse 'HEAD^{tree}')"
[ "$(git rev-parse HEAD)" = "$H" ] && echo "head: OK" || echo "head: MISMATCH"
s=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$s" ] && echo "status --porcelain --ignored: empty" || { echo "status not clean:"; echo "$s"; }
# Index equals HEAD tree (mode, blob, path).
d=$(git diff-index --cached HEAD)
[ -z "$d" ] && echo "index == HEAD tree: OK" || { echo "index differs:"; echo "$d"; }
# Every regular tracked file rehashes to its index blob; modes match.
n=0; bad=0; mbad=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    [ "$(readlink "$path" | tr -d '\n' | git hash-object --stdin)" = "$blob" ] || echo "SYMLINK MISMATCH $path"
    continue
  fi
  [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || echo "BLOB MISMATCH $path"
  if [ -x "$path" ]; then m=100755; else m=100644; fi
  [ "$m" = "$mode" ] || echo "MODE MISMATCH $path $mode $m"
done > "$T" 2>&1
echo "regular tracked files: $(git ls-files -s | awk '$1!=160000 && $1!=120000' | wc -l); mismatches: $(wc -l < "$T")"
cat "$T"; rm -f "$T"
echo "gitlinks (HEAD tree vs index):"
git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
git ls-files -s external gptp-processor protocol-processor third_party/verilog-axis
