#!/usr/bin/env bash
# Scratch launcher (never committed): run one Vivado batch script in its directory, for use ONLY inside a
# caller that already holds the host's shared Vivado lock; records start, end and rc beside the log.
#   run_vivado_held.sh <dir> <tcl> <log> [tclargs...]
set -u
dir=$1; tcl=$2; log=$3; shift 3
export PATH="$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH"
cd "$dir" || exit 2
date -Is > "$log.start"
rc=0
nice -n 10 vivado -mode batch -source "$tcl" -nojournal -log "$log" -tclargs "$@" > "$log.stdout" 2>&1 || rc=$?
date -Is > "$log.end"
echo "$rc" > "$log.rc"
exit "$rc"
