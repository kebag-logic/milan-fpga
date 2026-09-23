#!/usr/bin/env bash
# Reviewer-owned post-probe integrity check of the review clone (issue 439).
# Usage: verify_integrity.sh <clone> <expected-head> <expected-tree>
# Verifies HEAD/tree, a clean worktree and index (ignored files included),
# that every tracked path's index entry equals HEAD's tree entry (mode+blob),
# that every tracked regular file on disk hashes to its blob and every
# symlink's target hashes to its blob, that no index entry carries the
# assume-unchanged or skip-worktree flag, and that the three required
# submodules sit clean at their gitlinks.
set -euo pipefail
clone=$1 want_head=$2 want_tree=$3
cd "$clone"
export GIT_NO_REPLACE_OBJECTS=1
fail=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "head=$head tree=$tree"
[ "$head" = "$want_head" ] || { echo "FAIL head"; fail=1; }
[ "$tree" = "$want_tree" ] || { echo "FAIL tree"; fail=1; }
st=$(git status --porcelain=v2 --ignored --untracked-files=all)
[ -z "$st" ] || { echo "FAIL status: $st"; fail=1; }
git diff --quiet || { echo "FAIL worktree diff"; fail=1; }
git diff --cached --quiet || { echo "FAIL index diff"; fail=1; }
diff <(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort) \
     <(git ls-files -s | awk '{print $1, $2, $4}' | sort) >/dev/null \
  || { echo "FAIL index != HEAD tree (mode/blob/path)"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' || true)
[ -z "$flags" ] || { echo "FAIL index flags: $flags"; fail=1; }
n=0 bad=0
while read -r mode blob path; do
  case "$mode" in
    160000) continue ;;
    120000) got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin) ;;
    *) got=$(git hash-object --no-filters -- "$path")
       if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "FAIL mode $path"; bad=$((bad+1)); fi
       if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "FAIL mode $path"; bad=$((bad+1)); fi ;;
  esac
  n=$((n+1))
  [ "$got" = "$blob" ] || { echo "FAIL bytes $path"; bad=$((bad+1)); }
done < <(git ls-tree -r --full-tree HEAD | awk -F'\t' '{split($1,a," "); print a[1], a[3], $2}')
echo "tracked_non_gitlink_entries_verified=$n byte_or_mode_failures=$bad"
[ "$bad" = 0 ] || fail=1
for sub in third_party/verilog-axis protocol-processor gptp-processor; do
  pin=$(git ls-tree HEAD "$sub" | awk '{print $3}')
  got=$(git -C "$sub" rev-parse HEAD)
  sst=$(git -C "$sub" status --porcelain --ignored --untracked-files=all)
  echo "submodule $sub pin=$pin head=$got clean=$([ -z "$sst" ] && echo yes || echo no)"
  [ "$pin" = "$got" ] && [ -z "$sst" ] || fail=1
done
echo "RESULT=$([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
