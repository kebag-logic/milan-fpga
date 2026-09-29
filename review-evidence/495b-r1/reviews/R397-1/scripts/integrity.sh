#!/bin/bash
# Prove the review clone is exactly the published head: HEAD, index-vs-tree,
# every tracked blob's bytes and mode on disk, required gitlinks, no stray files.
# Usage: integrity.sh <clone> <expected-head>
set -euo pipefail
C=$1; H=$2
cd "$C"
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD mismatch"; exit 1; }
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
# index equals HEAD tree
[ "$(git write-tree)" = "$(git rev-parse HEAD^{tree})" ] || { echo "index != HEAD tree"; exit 1; }
echo "index write-tree matches HEAD tree"
# every tracked regular file / symlink: hash on-disk bytes, compare with the tree; mode too
bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; type=$2; oid=$3
  case "$type" in
    blob)
      if [ "$mode" = 120000 ]; then
        got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
        [ -L "$path" ] || { echo "not symlink: $path"; bad=1; continue; }
      else
        [ -f "$path" ] && [ ! -L "$path" ] || { echo "not file: $path"; bad=1; continue; }
        got=$(git hash-object --no-filters "$path")
        if [ -x "$path" ]; then dm=100755; else dm=100644; fi
        [ "$dm" = "$mode" ] || { echo "mode $path $dm != $mode"; bad=1; }
      fi
      [ "$got" = "$oid" ] || { echo "bytes $path"; bad=1; } ;;
    commit)
      got=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo uninit)
      echo "gitlink $path $oid checkout=$got"
      if [ "$path" != external ]; then [ "$got" = "$oid" ] || { echo "gitlink mismatch $path"; bad=1; }; fi ;;
  esac
done < <(git ls-tree -r --full-tree HEAD)
n=$(git ls-files | wc -l)
echo "tracked entries checked: $n"
extra=$(git status --porcelain --ignored --untracked-files=all | grep -v '^!! external/' || true)
[ -z "$extra" ] || { echo "status not clean:"; echo "$extra"; bad=1; }
for s in gptp-processor protocol-processor third_party/verilog-axis; do
  st=$(git -C "$s" status --porcelain --ignored --untracked-files=all)
  [ -z "$st" ] || { echo "submodule $s dirty:"; echo "$st" | head; bad=1; }
done
[ $bad = 0 ] && echo "INTEGRITY OK" || { echo "INTEGRITY FAIL"; exit 1; }
