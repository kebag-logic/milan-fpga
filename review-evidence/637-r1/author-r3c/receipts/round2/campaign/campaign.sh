#!/usr/bin/env bash
cd <scratch>/gates || exit 2
export TMPDIR=<scratch>/r2/tmp
export PATH=<tools>/pinned-verilator-5.050:$PATH
date -u +%FT%TZ; git rev-parse HEAD; git status --short; verilator --version; python3 --version
rc=0
make -C tb/verilator/milan_dp dynmap-mutants VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2 DYNMAP_MUTANT_JOBS=4 || rc=$?
echo "CAMPAIGN rc=$rc"; date -u +%FT%TZ
