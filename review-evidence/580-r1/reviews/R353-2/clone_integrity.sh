#!/bin/bash
# Verify a review clone is byte-exact at its head: tree, index, every tracked
# blob and mode, flags, untracked/ignored residue, and submodule gitlinks.
# Usage: clone_integrity.sh <repo> <expected-head> <expected-tree>
set -u
R=$1; H=$2; T=$3; rc=0; cd "$R" || exit 2
say() { echo "$1"; }
[ "$(git rev-parse HEAD)" = "$H" ] && say "HEAD $H" || { say "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && say "tree $T" || { say "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$T" ] && say "index tree equals head tree" || { say "INDEX MISMATCH"; rc=1; }
git update-index -q --really-refresh >/dev/null 2>&1
git diff --quiet HEAD && say "worktree equals HEAD" || { say "WORKTREE DIFF"; rc=1; }
git diff --cached --quiet && say "index equals HEAD" || { say "STAGED DIFF"; rc=1; }
flags=$(git ls-files -v | grep -c '^[a-z]\|^S' || true); say "assume-unchanged/skip-worktree entries: $flags"; [ "$flags" = 0 ] || rc=1
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; sha=$2
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(readlink -n -- "$path" | git hash-object --stdin); else got=$(git hash-object --no-filters -- "$path"); fi
  [ "$got" = "$sha" ] || { say "BLOB MISMATCH $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then say "MODE MISMATCH $path"; bad=$((bad+1)); fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then say "MODE MISMATCH $path"; bad=$((bad+1)); fi
done < <(git ls-files -s | awk '{print $1" "$2"\t"substr($0, index($0,$4))}')
say "tracked blobs rehashed: $n; mismatches: $bad"; [ "$bad" = 0 ] || rc=1
say "untracked (not ignored): $(git ls-files --others --exclude-standard | wc -l)"
say "ignored: $(git ls-files --others --ignored --exclude-standard | wc -l)"
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  link=$(git rev-parse "HEAD:$sm"); head=$(git -C "$sm" rev-parse HEAD)
  dirty=$(git -C "$sm" status --porcelain --ignored | wc -l)
  say "submodule $sm gitlink $link checkout $head dirty/ignored entries $dirty"
  [ "$link" = "$head" ] && [ "$dirty" = 0 ] || rc=1
done
say "submodule external gitlink $(git rev-parse HEAD:external) (uninitialized at start)"
say "RESULT: $([ $rc = 0 ] && echo PASS || echo FAIL)"
exit $rc
