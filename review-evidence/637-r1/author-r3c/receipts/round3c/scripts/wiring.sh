#!/usr/bin/env bash
# the [762-DP] wiring mutants on obj_dynmap from a clean clone: the suite's ROM images first, then the driver
# usage: wiring.sh <clone> <logdir>
set -u
cd "$1" || exit 2
out=$2; mkdir -p "$out"
export TMPDIR=<scratch>/r3c/tmp
export PATH=<tools>/pinned-verilator-5.050:$PATH
{ date -u +%FT%TZ; git rev-parse HEAD; git status --short; verilator --version; python3 --version; } > "$out/wiring-identity.txt" 2>&1
make -C tb/verilator/milan_dp ltn_rom.hex ucode.hex > "$out/roms.log" 2>&1
echo "ROMS rc=$?" >> "$out/roms.log"
python3 -I <scratch>/r3c/scripts/wiring_mutants.py "$1" "$out/work" > "$out/wiring.log" 2>&1
echo "WIRING rc=$?" >> "$out/wiring.log"
date -u +%FT%TZ >> "$out/wiring-identity.txt"
