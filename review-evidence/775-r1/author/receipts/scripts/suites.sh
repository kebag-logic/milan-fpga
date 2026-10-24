#!/bin/bash
# suites.sh <clone> <out>: the two touched suites through their own Makefiles
# (crf_rx: unit, discontinuity, talker step, mutants.py; avtp_rxmon: flat, NX,
# lockstep N=1/N=8, lockstep_mutants.py, format_mutants.py), one log and rc each
. <out>/receipts/env.sh
cd "$1" || exit 2
out=$2; mkdir -p "$out"
{ git rev-parse HEAD; git status --porcelain --untracked-files=no; verilator --version; python3 --version; make --version | head -1; } > "$out/env.txt" 2>&1
make -C tb/verilator/crf_rx > "$out/crf_rx.log" 2>&1; echo "crf_rx rc=$?" >> "$out/rc.txt"
make -C tb/verilator/avtp_rxmon > "$out/avtp_rxmon.log" 2>&1; echo "avtp_rxmon rc=$?" >> "$out/rc.txt"
cat "$out/rc.txt"
