#!/bin/sh
# R602-2: prove a review clone holds exact head bytes after the probes.
# Usage: verify_clone.sh CLONE HEAD_SHA HEAD_TREE
# Checks: HEAD and its tree; the index tree (git write-tree) equals HEAD's;
# every tracked regular file and symlink rehashes (git hash-object, no
# filters) to its index blob, with its mode; no untracked or ignored files;
# each initialised submodule's checkout equals its gitlink and is clean.
set -u
clone=$1; head=$2; tree=$3
fail=0
cd "$clone" || exit 2
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD differs"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] || { echo "HEAD tree differs"; fail=1; }
[ "$(git write-tree)" = "$tree" ] && echo "index tree = $tree" || { echo "index tree differs"; fail=1; }
n=0; bad=0
git ls-files -s | while read -r mode blob stage path; do
	case $mode in
	160000) continue ;;
	120000) got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin) ;;
	*) got=$(git hash-object --no-filters -- "$path")
	   if [ -x "$path" ]; then fm=100755; else fm=100644; fi
	   [ "$fm" = "$mode" ] || { echo "MODE $path $fm != $mode"; echo x >> /tmp/r602_2_verify_bad.$$; } ;;
	esac
	[ "$got" = "$blob" ] || { echo "BYTES $path"; echo x >> /tmp/r602_2_verify_bad.$$; }
done
if [ -s /tmp/r602_2_verify_bad.$$ ]; then fail=1; fi
rm -f /tmp/r602_2_verify_bad.$$
echo "tracked files rehashed: $(git ls-files -s | grep -vc '^160000')"
extra=$(git status --porcelain --ignored --untracked-files=all | wc -l)
echo "status entries (untracked/ignored/modified): $extra"
[ "$extra" -eq 0 ] || fail=1
git ls-files -s | awk '$1 == "160000" {print $2, $4}' | while read -r pin path; do
	if [ -e "$path/.git" ]; then
		co=$(git -C "$path" rev-parse HEAD)
		dirty=$(git -C "$path" status --porcelain --ignored | wc -l)
		echo "gitlink $path pin $pin checkout $co dirty-entries $dirty"
		{ [ "$co" = "$pin" ] && [ "$dirty" -eq 0 ]; } || echo "SUBMODULE MISMATCH $path"
	else
		echo "gitlink $path pin $pin (not initialised)"
	fi
done
if git ls-files -s | awk '$1 == "160000" {print $2, $4}' | while read -r pin path; do
	[ -e "$path/.git" ] || continue
	[ "$(git -C "$path" rev-parse HEAD)" = "$pin" ] || echo bad
	[ "$(git -C "$path" status --porcelain --ignored | wc -l)" -eq 0 ] || echo bad
done | grep -q bad; then fail=1; fi
[ $fail -eq 0 ] && echo "VERIFY OK" || echo "VERIFY FAILED"
exit $fail
