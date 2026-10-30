#!/usr/bin/env bash
# Run the head gates concurrently, each in its own archive copy of the clone.
# Usage: head_gates.sh <clone> <scratch-dir> <receipts-dir> <pinned-verilator-dir>
set -u
SRC=$1; WORK=$2; OUT=$3; VDIR=$4
mkdir -p "$WORK" "$OUT"
gate() { # name command...
  local name=$1; shift
  rm -rf "$WORK/g-$name"; mkdir -p "$WORK/g-$name"
  git -C "$SRC" archive HEAD | tar -x -C "$WORK/g-$name"
  ( cd "$WORK/g-$name" && "$@" ) > "$OUT/head_$name.log" 2>&1
  echo $? > "$OUT/head_$name.rc"
}
gate docs make -j16 docs &
gate diagrams make -j16 diagrams-check &
gate contract make -j16 contract &
gate lint env PATH="$VDIR:$PATH" make -j16 lint &
wait
git -C "$SRC" diff --check 135afd043309369a87ddbc8d6550aff8ec52a157 HEAD > "$OUT/head_diffcheck.log" 2>&1
echo $? > "$OUT/head_diffcheck.rc"
git -C "$SRC" diff --check 806957b35c3c23a36505744d205f9692720d19e2 HEAD >> "$OUT/head_diffcheck.log" 2>&1
echo $? >> "$OUT/head_diffcheck.rc"
for f in "$OUT"/head_*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(tr '\n' ' ' < "$f")"; done
