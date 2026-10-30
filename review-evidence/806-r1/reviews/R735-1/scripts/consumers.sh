#!/usr/bin/env bash
# Run the other gPTP consumer suites on one disposable copy of the reviewed
# clone, each with its own log and rc file.
# Usage: consumers.sh <clone> <packet>
set -u
clone=$1 packet=$2
vl=${PROBE_VERILATOR:-verilator}
tree=$packet/scratch/trees/S1
out=$packet/receipts/consumers
mkdir -p "$out" "$packet/scratch/trees"
rm -rf "$tree"
cp -a "$clone" "$tree" || exit 2
one() { # <name> <dir> <target>
  /usr/bin/time -v make -C "$tree/tb/verilator/$2" VERILATOR="$vl" "$3" \
    >"$out/$1.log" 2>&1
  echo $? >"$out/$1.rc"
}
one gptp_shadow gptp_shadow run &
one gptp_plane gptp_plane run &
one gptp_txts gptp_txts run &
one gmstep milan_dp gmstep &
wait
git -C "$tree" status --short >"$out/tree-status-after.txt" 2>&1
