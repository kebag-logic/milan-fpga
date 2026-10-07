#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Reviewer static checks for lwSRP PR #3: scope, commit shape, SPDX, privacy,
# clone integrity at the exact reviewed head.
# Usage: checks.sh <lwsrp-clone>   (prints the receipt to stdout)
set -u
cd "$1" || exit 2
HEAD=e4f9995b791489c53b8ccb8a8dc09ec508e32e6b
BASE=19f5796b63652eb1151906de73cb827d4980a53f
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse 'HEAD^{tree}')"
[ "$(git rev-parse HEAD)" = "$HEAD" ] && echo "exact_head=OK"
echo "== changed files $BASE..$HEAD"
git diff --name-status "$BASE..$HEAD"
echo "== protocol/zephyr/doc paths changed (expect none)"
git diff --name-only "$BASE..$HEAD" -- src zephyr Kconfig.zephyr doc README.md
echo "== codec test and scenario sources unchanged (expect none)"
git diff --name-only "$BASE..$HEAD" -- tests/unit/mrp_pdu_test.c tests/features/switch.feature tests/features/steps
echo "== commits in range: sha|author|committer|parents"
git log --format='%H|%an <%ae>|%cn <%ce>|%P' "$BASE..$HEAD"
echo "== identity of earlier repository commits"
git log --format='%an <%ae>' "$BASE" -3
echo "== commit message (cat -A)"
git log -1 --format=%B "$HEAD" | cat -A
echo "== SPDX first line of added files"
for f in $(git diff --name-only --diff-filter=A "$BASE..$HEAD"); do
    printf '%s: %s\n' "$f" "$(head -1 "$f")"
done
echo "== privacy scan of diff and message (expect no hits)"
# Host-path pattern; PRIVACY_EXTRA may add an alternation of tool or account
# names supplied by the reviewer (kept out of this public script).
PAT='/home/|/data/|/tmp/|/Users/'
[ -n "${PRIVACY_EXTRA:-}" ] && PAT="$PAT|$PRIVACY_EXTRA" && echo "extra_terms_supplied=yes"
( git diff "$BASE..$HEAD"; git log -1 --format=%B "$HEAD" ) | grep -n -iE "$PAT"
echo "privacy_grep_rc=$? (1 = no hits)"
echo "== gitlinks in tree (expect 0)"
git ls-tree -r HEAD | awk '$1=="160000"' | wc -l
echo "== clone integrity"
echo "porcelain_ignored_entries=$(git status --porcelain --ignored | wc -l)"
git diff --quiet && git diff --cached --quiet && echo "index_and_worktree_clean=OK"
diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') && echo "index_matches_tree=OK"
diff <(git ls-tree -r HEAD | awk '{print $3, $4}' | sort -k2) \
     <(git ls-files -z | xargs -0 git hash-object | paste -d' ' - <(git ls-files) | sort -k2) && echo "worktree_blobs_match=OK"
bad=0
for f in $(git ls-files); do
    m=$(stat -c %a "$f"); t=$(git ls-tree HEAD -- "$f" | awk '{print $1}')
    case "$t$m" in 100644644|100755755) ;; *) echo "mode_mismatch $f $t $m"; bad=1;; esac
done
[ $bad = 0 ] && echo "worktree_modes_match=OK"
