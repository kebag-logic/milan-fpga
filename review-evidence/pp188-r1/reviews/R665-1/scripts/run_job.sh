#!/usr/bin/env bash
# usage: run_job.sh <out dir> <name> <workdir> <command...>
# Runs one command with the pinned Verilator first on PATH and scratch TMPDIR;
# writes <name>.log, its own exit status to <name>.rc (never through a pipe),
# and wall seconds to <name>.sec.
set -u
out=$1; name=$2; wd=$3; shift 3
P=$(cd "$(dirname "$0")/.." && pwd)   # the packet root
export PATH=$P/scratch/bin:$PATH TMPDIR=$P/scratch/tmp VERILATOR=$P/scratch/bin/verilator
mkdir -p "$out"
t0=$(date +%s)
( cd "$wd" && "$@" ) > "$out/$name.log" 2>&1
echo $? > "$out/$name.rc"
echo $(( $(date +%s) - t0 )) > "$out/$name.sec"
