#!/bin/bash
# Verify the review clone equals the exact head: tracked bytes/modes/index, no residue, gitlinks.
set -u; R=$1; H=$2; cd $R
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) expected $H"
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD MISMATCH"; exit 1; }
git update-index -q --really-refresh
echo "index-tree $(git write-tree)"
[ "$(git write-tree)" = "$(git rev-parse HEAD^{tree})" ] || { echo "INDEX != HEAD TREE"; exit 1; }
d=$(git diff --name-only HEAD; git diff --cached --name-only HEAD); [ -z "$d" ] || { echo "DIFF: $d"; exit 1; }
u=$(git status --porcelain --ignored --untracked-files=all -- . ':!third_party/lwSRP' ':!protocol-processor' ':!gptp-processor' ':!third_party/verilog-axis'); [ -z "$u" ] || { echo "RESIDUE: $u"; exit 1; }
flags=$(git ls-files -v | grep -v '^H ' | head); [ -z "$flags" ] || { echo "INDEX FLAGS: $flags"; exit 1; }
git ls-files -s | awk '$1!="160000"{print $1, $2, $4}' > /tmp/r532-ls.$$; bad=0
while read -r mode sha path; do
  [ "$(git hash-object --no-filters -- "$path")" = "$sha" ] || { echo "BLOB MISMATCH $path"; bad=1; }
  case $mode in 100755) [ -x "$path" ] || { echo "MODE $path"; bad=1; };; 100644) [ -x "$path" ] && { echo "MODE $path"; bad=1; };; 120000) [ -L "$path" ] || { echo "LINK $path"; bad=1; };; esac
done < /tmp/r532-ls.$$; rm -f /tmp/r532-ls.$$
echo "tracked files: $(git ls-files | wc -l) blob/mode bad=$bad"
for sm in third_party/lwSRP protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD $sm | awk '{print $3}'); have=$(git -C $sm rev-parse HEAD 2>/dev/null || echo uninit)
  st=$(git -C $sm status --porcelain --ignored 2>/dev/null | head -3)
  echo "gitlink $sm want=$want have=$have $( [ "$want" = "$have" ] && echo OK || echo MISMATCH) clean=$([ -z "$st" ] && echo yes || echo NO)"
done
exit $bad
