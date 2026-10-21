#!/usr/bin/env bash
# make -C tb/verilator/milan_dp (every leg) from a clean clone, one log and one rc
# usage: milan-dp-all.sh <clone> <logdir>
set -u
cd "$1" || exit 2
out=$2; mkdir -p "$out"
export TMPDIR=<scratch>/r3c/tmp
export PATH=<tools>/pinned-verilator-5.050:$PATH
{ date -u +%FT%TZ; git rev-parse HEAD; git status --short; verilator --version; python3 --version; } > "$out/milan-dp-identity.txt" 2>&1
make -C tb/verilator/milan_dp VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2 > "$out/milan-dp-all.log" 2>&1
echo "MILAN_DP rc=$?" >> "$out/milan-dp-all.log"
date -u +%FT%TZ >> "$out/milan-dp-identity.txt"
