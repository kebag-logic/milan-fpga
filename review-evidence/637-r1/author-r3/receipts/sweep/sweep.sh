#!/usr/bin/env bash
cd <scratch>/gates || exit 2
export TMPDIR=<scratch>/tmp
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2 SIM_JOBS=2 MAKEFLAGS="-j2 --no-print-directory"
date -u +%FT%TZ; git rev-parse HEAD; git status --short; verilator --version; python3 --version
out=<scratch>/sweep-logs; rm -rf "$out"; mkdir -p "$out"
rc=0; scripts/run_all_suites.sh "$out" || rc=$?
echo "SWEEP rc=$rc"; date -u +%FT%TZ
