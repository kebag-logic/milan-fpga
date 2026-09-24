#!/usr/bin/env bash
# Integrity fingerprint of a clone at an exact head: HEAD, tree, index hash,
# a per-file comparison of worktree bytes and modes against HEAD's blobs, the
# submodule gitlinks and their checked-out revisions, and untracked files.
# Usage: integrity.sh <repo> <expected-head>
set -euo pipefail
repo=$1 want=$2
g() { git -C "$repo" "$@"; }
head=$(g rev-parse HEAD)
echo "HEAD      $head"
echo "expected  $want"
[ "$head" = "$want" ] && echo "HEAD MATCH" || echo "HEAD MISMATCH"
echo "tree      $(g rev-parse HEAD^{tree})"
# The raw index file carries a stat cache that `git status`/`git diff` refresh
# in place, so its file hash moves without any entry changing; the entry-level
# hash (mode, object id, stage, path) is the invariant compared across runs.
echo "index-file-sha256 (volatile stat cache) $(sha256sum "$(g rev-parse --absolute-git-dir)/index" | cut -d' ' -f1)"
echo "index-entries-sha256 $(g ls-files -s | sha256sum | cut -d' ' -f1)"
echo "HEAD-tree-entries-sha256 $(g ls-tree -r --full-tree HEAD | awk '{print $1" "$3" 0\t"$4}' | sha256sum | cut -d' ' -f1)"
# every index entry must be stage 0 and equal HEAD's entry (mode, oid, path)
diff <(g ls-files -s | sort) <(g ls-tree -r --full-tree HEAD | awk '{print $1" "$3" 0\t"$4}' | sort) \
  >/dev/null && echo "index == HEAD tree (mode/oid/path, stage 0)" || echo "index DIFFERS from HEAD tree"
# worktree bytes: re-hash every regular tracked file and compare to HEAD blob
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  [ "$type" = blob ] || continue
  n=$((n+1))
  f="$repo/$path"
  if [ "$mode" = 120000 ]; then
    [ -L "$f" ] && [ "$(printf %s "$(readlink "$f")" | git hash-object --stdin)" = "$oid" ] || { echo "SYMLINK DIFF $path"; bad=$((bad+1)); }
    continue
  fi
  [ -f "$f" ] && [ ! -L "$f" ] || { echo "MISSING $path"; bad=$((bad+1)); continue; }
  h=$(git hash-object --no-filters "$f")
  [ "$h" = "$oid" ] || { echo "BYTES DIFF $path"; bad=$((bad+1)); }
  if [ -x "$f" ]; then m=100755; else m=100644; fi
  [ "$m" = "$mode" ] || { echo "MODE DIFF $path want $mode have $m"; bad=$((bad+1)); }
done < <(g ls-tree -r --full-tree HEAD)
echo "tracked blobs checked: $n, differences: $bad"
echo "## gitlinks (HEAD) vs checked-out"
g ls-tree -r --full-tree HEAD | awk '$2=="commit"{print $3" "$4}' | while read -r oid p; do
  if [ -e "$repo/$p/.git" ]; then co=$(git -C "$repo/$p" rev-parse HEAD); else co=UNINITIALISED; fi
  echo "$p gitlink=$oid checkout=$co $([ "$oid" = "$co" ] && echo OK || { [ "$p" = external ] && [ "$co" = UNINITIALISED ] && echo "NOT-INITIALISED (SSH-only, read by no gate; expected)" || echo DIFF; })"
done
echo "## untracked, not ignored (superproject)"
g ls-files --others --exclude-standard | head -50
echo "## status --porcelain (superproject, submodules summarised)"
g status --porcelain=v1 --ignore-submodules=none | head -50
echo "## submodule dirty check"
for p in protocol-processor gptp-processor third_party/verilog-axis; do
  echo "$p: $(git -C "$repo/$p" status --porcelain=v1 | wc -l) status lines"
done
