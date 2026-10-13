#!/bin/sh
# Reviewer restore check for a checkout ($1) against the exact head ($2): index equals HEAD's tree,
# every tracked regular file and symlink hashes to its blob with its mode, no index flag hides an edit,
# no untracked or ignored residue, and every initialised submodule sits at its gitlink, clean.
set -u
cd "$1" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$2" ] || { echo "HEAD is not $2"; fail=1; }
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/.vr_index.$$
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort > /tmp/.vr_tree.$$
cmp -s /tmp/.vr_index.$$ /tmp/.vr_tree.$$ && echo "index == HEAD tree ($(wc -l < /tmp/.vr_tree.$$) entries)" || { echo "index differs from HEAD tree"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' | wc -l); echo "index entries with flags other than H: $flags"; [ "$flags" = 0 ] || fail=1
bad=0
git ls-files -s | while read mode blob stage path; do
  case "$mode" in
    160000) continue ;;
    120000) h=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); [ -L "$path" ] || h=notlink ;;
    100755) [ -x "$path" ] && [ ! -L "$path" ] || { echo "MODE $path"; }; h=$(git hash-object --no-filters "$path") ;;
    100644) [ ! -x "$path" ] && [ ! -L "$path" ] || { echo "MODE $path"; }; h=$(git hash-object --no-filters "$path") ;;
  esac
  [ "$h" = "$blob" ] || echo "BYTES $path"
done > /tmp/.vr_bad.$$
n=$(wc -l < /tmp/.vr_bad.$$); echo "tracked files with byte or mode mismatch: $n"; [ "$n" = 0 ] || { head /tmp/.vr_bad.$$; fail=1; }
res=$(git status --porcelain --ignored | wc -l); echo "untracked/ignored/modified entries: $res"; [ "$res" = 0 ] || { git status --porcelain --ignored | head; fail=1; }
git ls-files -s | awk '$1=="160000"{print $2, $4}' | while read link path; do
  if [ -e "$path/.git" ]; then
    h=$(git -C "$path" rev-parse HEAD); d=$(git -C "$path" status --porcelain --ignored | wc -l)
    echo "submodule $path gitlink $link HEAD $h dirty-entries $d $( [ "$h" = "$link" ] && [ "$d" = 0 ] && echo OK || echo BAD)"
  else echo "submodule $path gitlink $link not initialised"; fi
done | tee /tmp/.vr_sub.$$
grep -q " BAD$" /tmp/.vr_sub.$$ && fail=1
rm -f /tmp/.vr_*.$$
echo "verify_restore: $( [ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
