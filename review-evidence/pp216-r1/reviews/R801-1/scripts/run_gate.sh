#!/usr/bin/env bash
# run_gate.sh NAME WORKDIR CMD... : run CMD in WORKDIR, record cmd, log, rc, start/end epoch.
# Usage is portable: set VERILATOR_DIR to a Verilator 5.050 bin dir; OUT defaults to ../receipts.
set -u
name=$1; wd=$2; shift 2
out=${OUT:-$(cd "$(dirname "$0")/.." && pwd)/receipts}
mkdir -p "$out"
[ -n "${VERILATOR_DIR:-}" ] && export PATH="$VERILATOR_DIR:$PATH"
printf '%q ' "$@" > "$out/$name.cmd"; echo >> "$out/$name.cmd"
date +%s > "$out/$name.start"
( cd "$wd" && "$@" ) > "$out/$name.log" 2>&1
echo $? > "$out/$name.rc"
date +%s > "$out/$name.end"
