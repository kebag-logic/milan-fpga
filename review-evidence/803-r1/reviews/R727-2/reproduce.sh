#!/bin/sh
# usage: reproduce.sh <clean clone at 2b1565fd, submodules checked out> <workdir>
# Re-plants this round's probes, one per disposable copy, builds and runs the
# milan_dp gptp leg (and the clean gptp-lat leg) concurrently, and prints the
# FAIL lines and tallies. Set VERILATOR to the pinned Verilator 5.050.
set -u
SRC="$1"; W="$2"; HERE=$(cd "$(dirname "$0")" && pwd); R="$W/receipts"
mkdir -p "$R"
[ "$(git -C "$SRC" rev-parse HEAD)" = 2b1565fd9095d6ec8be514849ba9b92b8f4c5b31 ] || { echo "wrong head"; exit 2; }
for p in clean m9 m9b m9c s1-no-held-req h1-no-hold; do
  rm -rf "$W/$p"; cp -a "$SRC" "$W/$p"
  [ "$p" = clean ] || git -C "$W/$p" apply "$HERE/receipts/probe-$p.diff" || exit 3
done
for spec in "clean gptp" "clean gptp-lat" "m9 gptp" "m9b gptp" "m9c gptp" \
            "s1-no-held-req gptp" "h1-no-hold gptp"; do
  set -- $spec
  "$HERE/run_leg.sh" "$W/$1" "$2" "$R/$1-$2.log" "$R/$1-$2.rc" &
done
wait
for f in "$R"/*.log; do
  echo "== $(basename "$f") rc=$(cat "${f%.log}.rc")"
  grep -E "^FAIL|^\[cut\]|^\[#207\]|checks:" "$f"
done
