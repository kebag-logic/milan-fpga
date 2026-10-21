#!/usr/bin/env bash
# the full dynmap-mutants campaign from a clean clone, the listener suite's clean build first
# usage: campaign.sh <clone> <logdir>
set -u
cd "$1" || exit 2
out=$2; mkdir -p "$out"
export TMPDIR=<scratch>/r3c/tmp
export PATH=<tools>/pinned-verilator-5.050:$PATH
{ date -u +%FT%TZ; git rev-parse HEAD; git status --short; verilator --version; python3 --version; } > "$out/campaign-identity.txt" 2>&1
make -C tb/verilator/milan_dp_render tdm8render-build VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2 > "$out/render-build.log" 2>&1
echo "RENDER-BUILD rc=$?" >> "$out/render-build.log"
make -C tb/verilator/milan_dp dynmap-mutants VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2 DYNMAP_MUTANT_JOBS=4 > "$out/campaign.log" 2>&1
echo "CAMPAIGN rc=$?" >> "$out/campaign.log"
date -u +%FT%TZ >> "$out/campaign-identity.txt"
