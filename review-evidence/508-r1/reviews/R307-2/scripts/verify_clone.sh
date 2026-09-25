#!/bin/sh
# Verify the review clone is at the exact head with pristine tracked bytes,
# modes, index and gitlinks. Usage: verify_clone.sh <clone>
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "HEAD tree $(git rev-parse 'HEAD^{tree}')"
echo "index tree $(git write-tree)"
git update-index -q --really-refresh
echo "unstaged diff files: $(git diff --name-only | wc -l)"
echo "staged diff files: $(git diff --cached --name-only | wc -l)"
echo "status (incl. ignored) entries: $(git status --porcelain --ignored | wc -l)"
# re-hash every tracked regular blob from the working tree and compare with HEAD
bad=0; n=0
git ls-tree -r HEAD | while read -r mode type sha path; do
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then w=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); else w=$(git hash-object "$path"); fi
  fm=$(stat -c %a "$path" 2>/dev/null)
  case "$mode" in 100755) em=755;; 100644) em=644;; *) em=$fm;; esac
  if [ "$w" != "$sha" ]; then echo "BLOB MISMATCH $path"; fi
  if [ "$mode" != 120000 ] && [ "$(( 0$fm & 0100 ))" -ne "$(( 0$em & 0100 ))" ]; then echo "MODE MISMATCH $path $fm vs $mode"; fi
done > /tmp/.r307_2_verify.$$
echo "tracked blobs: $(git ls-tree -r HEAD | awk '$2=="blob"' | wc -l); mismatches: $(wc -l < /tmp/.r307_2_verify.$$)"
cat /tmp/.r307_2_verify.$$; rm -f /tmp/.r307_2_verify.$$
git ls-tree -r HEAD | awk '$2=="commit"{print "gitlink", $4, $3}'
git submodule status | sed 's/ (.*)//'
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  echo "submodule $s status entries (incl. ignored): $(git -C $s status --porcelain --ignored | wc -l)"
done
