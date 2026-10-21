#!/usr/bin/env bash
# the milan_dp dynmap, maprec8 and maprec4 legs from a clean clone, one log and one rc each, at most two builds at once
# usage: legs.sh <clone> <logdir>
set -u
cd "$1" || exit 2
out=$2; mkdir -p "$out"
export TMPDIR=<scratch>/r3/tmp
export PATH=<tools>/pinned-verilator-5.050:$PATH
V=<tools>/pinned-verilator-5.050/verilator
{ date -u +%FT%TZ; git rev-parse HEAD; git status --short; verilator --version; } > "$out/legs-identity.txt" 2>&1
leg() {
  make -C tb/verilator/milan_dp "$1" VERILATOR=$V VERILATOR_JOBS=2 > "$out/leg-$1.log" 2>&1
  printf '%s\t%s\n' "$1" "$?" >> "$out/rc.tsv"
}
leg dynmap & leg maprec8 & wait
leg maprec4
date -u +%FT%TZ >> "$out/legs-identity.txt"
