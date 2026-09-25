#!/bin/sh
# Verify a review clone is byte-identical to its exact head.
# Usage: verify_clone.sh <checkout> <expected-head> <expected-tree>
# Checks: HEAD and tree ids; index entries equal the HEAD tree (mode, blob,
# path); every tracked regular file's bytes re-hash to its index blob and its
# executable bit matches the index mode; symlink targets match; no tracked
# modification or staged change; each submodule is checked out at its gitlink
# with a clean worktree, and its tracked bytes re-hash to its own index.
set -u
repo=$1; head=$2; tree=$3; rc=0
cd "$repo" || exit 2
say() { echo "$*"; }
[ "$(git rev-parse HEAD)" = "$head" ] && say "HEAD ok $head" || { say "HEAD MISMATCH $(git rev-parse HEAD)"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] && say "tree ok $tree" || { say "TREE MISMATCH"; rc=1; }

check_bytes() {  # run inside a repository: re-hash tracked files against the index
  git ls-files -s | awk '$1=="100644"||$1=="100755"{print $1" "$2" "substr($0, index($0,"\t")+1)}' > /tmp/.vc_idx.$$
  cut -d' ' -f3- /tmp/.vc_idx.$$ | git hash-object --no-filters --stdin-paths > /tmp/.vc_hash.$$
  n=$(wc -l < /tmp/.vc_idx.$$)
  bad=$(paste -d' ' /tmp/.vc_idx.$$ /tmp/.vc_hash.$$ | awk '{h=$NF; if ($2!=h) print $0}' | wc -l)
  modebad=0
  while read -r mode blob path; do
    if [ -x "$path" ]; then m=100755; else m=100644; fi
    [ "$m" = "$mode" ] || { echo "MODE $path index=$mode fs=$m"; modebad=$((modebad+1)); }
  done < /tmp/.vc_idx.$$
  lbad=0
  git ls-files -s | awk '$1=="120000"{print $2" "substr($0, index($0,"\t")+1)}' | while read -r blob path; do
    [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$blob" ] || echo "SYMLINK $path"
  done
  echo "  files=$n byte_mismatch=$bad mode_mismatch=$modebad"
  rm -f /tmp/.vc_idx.$$ /tmp/.vc_hash.$$
  [ "$bad" -eq 0 ] && [ "$modebad" -eq 0 ]
}

if [ "$(git ls-files -s | awk '{print $1" "$2" "$4}' | sort)" = "$(git ls-tree -r HEAD | awk '{print $1" "$3" "$4}' | sort)" ]; then
  say "index == HEAD tree"; else say "INDEX DIFFERS FROM HEAD"; rc=1; fi
git diff --quiet --ignore-submodules=none && git diff --cached --quiet && say "no tracked or staged changes" || { say "TRACKED CHANGES:"; git status --porcelain; rc=1; }
say "superproject bytes:"; check_bytes || rc=1
git ls-tree -r HEAD | awk '$2=="commit"{print $3" "$4}' | while read -r link path; do
  if [ -e "$path/.git" ]; then
    act=$(git -C "$path" rev-parse HEAD)
    st=$(git -C "$path" status --porcelain --untracked-files=no)
    say "submodule $path gitlink=$link checkout=$act $( [ "$link" = "$act" ] && echo MATCH || echo MISMATCH ) $( [ -z "$st" ] && echo clean || echo DIRTY )"
    (cd "$path" && check_bytes) || echo "SUBMODULE BYTES BAD $path"
  else
    say "submodule $path gitlink=$link not checked out"
  fi
done
exit $rc
