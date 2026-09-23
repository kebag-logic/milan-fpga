#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe: prove a review clone still holds exactly the published head.
#
# Usage: verify_clone.sh CLONE EXPECTED_COMMIT EXPECTED_TREE
# Checks: HEAD and its tree; index == HEAD tree (paths, modes, blob ids);
# every tracked working file re-hashed (no filters) == its index blob; every
# tracked file's executable bit == its index mode; no untracked or ignored
# path; gitlinks listed (and each initialised one at its recorded commit).
# Exit 0 only when all hold.
set -euo pipefail
clone=$1 commit=$2 tree=$3
cd "$clone"
fail=0
say() { echo "$*"; }
head=$(git rev-parse HEAD); htree=$(git rev-parse 'HEAD^{tree}')
say "HEAD $head"; say "tree $htree"
[ "$head" = "$commit" ] || { say "FAIL: HEAD != $commit"; fail=1; }
[ "$htree" = "$tree" ] || { say "FAIL: tree != $tree"; fail=1; }
itree=$(git write-tree)
say "index tree $itree"
[ "$itree" = "$tree" ] || { say "FAIL: index tree != HEAD tree"; fail=1; }
n=0 bad=0 modebad=0
while IFS=$'\t' read -r meta path; do
    mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
    [ "$mode" = 160000 ] && continue
    n=$((n + 1))
    if [ "$mode" = 120000 ]; then
        got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
    else
        got=$(git hash-object --no-filters -- "$path")
        if [ -x "$path" ]; then fm=100755; else fm=100644; fi
        [ "$fm" = "$mode" ] || { say "MODE MISMATCH $path index=$mode file=$fm"; modebad=$((modebad + 1)); }
    fi
    [ "$got" = "$blob" ] || { say "BLOB MISMATCH $path"; bad=$((bad + 1)); }
done < <(git ls-files -s)
say "tracked files re-hashed: $n; blob mismatches: $bad; mode mismatches: $modebad"
[ "$bad" -eq 0 ] && [ "$modebad" -eq 0 ] || fail=1
extra=$(git status --porcelain=v1 --ignored --untracked-files=all | wc -l)
say "untracked/ignored/modified entries: $extra"
[ "$extra" -eq 0 ] || { git status --porcelain=v1 --ignored --untracked-files=all | head -20; fail=1; }
links=$(git ls-files -s | awk '$1 == "160000"' | wc -l)
say "gitlinks in index: $links"
git ls-files -s | awk '$1 == "160000" {print "  " $2 " " $4}'
if [ "$links" -gt 0 ]; then git submodule status; fi
say "RESULT: $([ $fail -eq 0 ] && echo INTACT || echo NOT-INTACT)"
exit $fail
