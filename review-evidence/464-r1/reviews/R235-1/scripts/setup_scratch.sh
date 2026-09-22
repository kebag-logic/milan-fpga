#!/usr/bin/env bash
# R235: build isolated scratch extracts with `git archive` (reads objects only;
# never touches the review checkout's index, worktree or refs).
# Usage: setup_scratch.sh <review-checkout> <scratch-root>
set -euo pipefail
repo=${1:?review checkout}
root=${2:?scratch root}
mkdir -p "$root"
extract() {  # extract <label> <rev>
  local label=$1 rev=$2 dst="$root/$1"
  rm -rf "$dst"; mkdir -p "$dst"
  git -C "$repo" archive --format=tar "$rev" | tar -x -C "$dst"
  printf '%s %s %s\n' "$label" "$(git -C "$repo" rev-parse "$rev^{commit}")" \
    "$(git -C "$repo" rev-parse "$rev^{tree}")" >> "$root/EXTRACTS.txt"
}
: > "$root/EXTRACTS.txt"
extract head    a769d9dbc937fb324c4726e60dee5b2f7ad349e3   # PR head / candidate
extract base    88e9276b2a220c716f64a843f7e1eb8f9265e896   # first parent (dev + #507)
extract src     1576f0893ae9781074fffb105f5384fe774ff11e   # author head
extract srcbase ec34fcdee0ca9ffa63564a9af8ad70a3a618de29   # author base
extract b7d0    b7d0bbcd60eb485af4004fff81056fe26afa829c   # parent of da71309c
extract da71    da71309c7b5067c0cb43ceb211a364c5ab037202   # map renumbering
cat "$root/EXTRACTS.txt"
# git archive writes no submodule contents: record that the gitlink paths are empty
for d in head base; do
  for sm in protocol-processor gptp-processor third_party/verilog-axis external; do
    n=$(find "$root/$d/$sm" -mindepth 1 2>/dev/null | wc -l || true)
    echo "$d/$sm entries: $n"
  done
done
