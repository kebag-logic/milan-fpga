#!/bin/sh
# Build disposable probe trees for the R709-3 review of PR #204.
# usage: setup_trees.sh <processor clone> <scratch dir>
# head    : exact head 429c909 (git archive, the clone is never touched)
# oldrtl  : head benches with hdl/ taken from ebb1f001 (the previous reviewed head)
# m_<name>: head with one reviewer-owned mutant planted (plant_mutant.py)
set -eu
SRC=$1
OUT=$2
HEAD=429c909cb8a60398a2028436932e04b95dd0a0bd
PREV=ebb1f0010bde76c38cc5270a6366ee9e3157ec54
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
rm -rf "$OUT/head" "$OUT/oldrtl"
mkdir -p "$OUT/head" "$OUT/oldrtl"
git -C "$SRC" archive "$HEAD" | tar -x -C "$OUT/head"
git -C "$SRC" archive "$HEAD" | tar -x -C "$OUT/oldrtl"
rm -rf "$OUT/oldrtl/hdl"
git -C "$SRC" archive "$PREV" hdl | tar -x -C "$OUT/oldrtl"
for m in none_sticky record_holds_new_id epoch_never_ticks parked_txla_sends_new_value join_never_follows_leave; do
  rm -rf "$OUT/m_$m"
  mkdir -p "$OUT/m_$m"
  git -C "$SRC" archive "$HEAD" | tar -x -C "$OUT/m_$m"
  python3 -I "$HERE/plant_mutant.py" "$OUT/m_$m" "$m"
done
