#!/bin/sh
# R366-3 clone integrity after probes (read-only). Usage: clone_integrity.sh <clone>
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD 2>/dev/null) expect 6b2ebd1c435136966f84ffc16d28a80c7d6b9387"
echo "tree $(git rev-parse 'HEAD^{tree}' 2>/dev/null) expect 832c46b5efcf8e937e899c625f6df0ae59adef7b"
echo "index-tree $(git write-tree 2>/dev/null)"
echo "status (incl. untracked+ignored):"; git status --porcelain --ignored --untracked-files=all 2>/dev/null; echo "end status"
# every tracked blob: mode and content hash on disk equal the HEAD tree entry
git ls-tree -r HEAD 2>/dev/null | awk '$2=="blob"' > /tmp/r366_3_ls.$$
total=0; bad=0
while read -r mode type sha path; do
  total=$((total+1))
  if [ "$mode" = "120000" ]; then disk=$(readlink "$path" | tr -d '\n' | git hash-object --stdin 2>/dev/null); dmode=120000
  else disk=$(git hash-object --no-filters -- "$path" 2>/dev/null); if [ -x "$path" ]; then dmode=100755; else dmode=100644; fi; fi
  if [ "$disk" != "$sha" ] || [ "$dmode" != "$mode" ]; then bad=$((bad+1)); echo "MISMATCH $mode/$dmode $path"; fi
done < /tmp/r366_3_ls.$$
rm -f /tmp/r366_3_ls.$$
echo "tracked blobs: $total, mismatches: $bad"
echo "gitlinks (HEAD pin vs checked out):"
git ls-tree -r HEAD 2>/dev/null | awk '$2=="commit"{print $3, $4}' | while read -r pin path; do
  if [ -e "$path/.git" ]; then co=$(git -C "$path" rev-parse HEAD 2>/dev/null); else co="uninitialised(empty=$(ls -A "$path" 2>/dev/null | wc -l))"; fi
  if [ -e "$path/.git" ]; then dirty=$(git -C "$path" status --porcelain 2>/dev/null | wc -l); else dirty=n/a; fi
  echo "$path pin=$pin checkout=$co dirty_entries=$dirty"
done
