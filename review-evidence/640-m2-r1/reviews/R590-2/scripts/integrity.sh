#!/usr/bin/env bash
# R590-2: prove the review clone is byte-identical to the exact head after
# the probes. Usage: integrity.sh CLONE HEAD
set -u
CLONE="$1"; HEAD_SHA="$2"
cd "$CLONE" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
[ "$(git rev-parse HEAD)" = "$HEAD_SHA" ] && echo "head: matches" || echo "head: MISMATCH"
echo "status --porcelain --ignored lines: $(git status --porcelain --ignored | wc -l)"
git update-index -q --really-refresh
git diff --quiet && git diff --cached --quiet && echo "worktree/index diff: none" || echo "worktree/index diff: PRESENT"
a="$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -c1-64)"
b="$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -c1-64)"
echo "ls-files -s (mode blob path) sha256 $a"
echo "ls-tree -r HEAD (mode blob path) sha256 $b"
[ "$a" = "$b" ] && echo "index equals HEAD tree: yes" || echo "index equals HEAD tree: NO"
# every tracked regular file's bytes and mode against its blob
bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode="$1"; blob="$3"
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    [ "$(readlink "$path")" = "$(git cat-file blob "$blob")" ] || { echo "symlink differs: $path"; bad=1; }
    continue
  fi
  [ "$(git hash-object "$path")" = "$blob" ] || { echo "bytes differ: $path"; bad=1; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "mode differs: $path"; bad=1; }
  else [ -x "$path" ] && { echo "mode differs: $path"; bad=1; }; fi
done < <(git ls-tree -r HEAD)
[ "$bad" = 0 ] && echo "tracked bytes and modes: all equal" || echo "tracked bytes and modes: DIFFER"
git submodule status | sed 's/^/gitlink /'
for s in gptp-processor protocol-processor third_party/verilog-axis; do
  echo "submodule $s clean lines: $(git -C "$s" status --porcelain --ignored | wc -l)"
done
