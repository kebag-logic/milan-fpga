#!/usr/bin/env bash
# Scratch launcher (never committed): run one Vivado batch script in its
# directory under the host's shared Vivado lock, recording rc, start/end time.
#   run_vivado.sh <dir> <tcl> <log> [tclargs...]
set -u
dir=$1; tcl=$2; log=$3; shift 3
export PATH="$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH"
cd "$dir" || exit 2
date -Is > "$log.queued"
rc=0
flock /tmp/milan-vivado.lock bash -c 'date -Is > "$0.start"; nice -n 10 vivado -mode batch -source "$1" -nojournal -log "$0" -tclargs "${@:2}" > "$0.stdout" 2>&1' "$log" "$tcl" "$@" || rc=$?
date -Is > "$log.end"
echo "$rc" > "$log.rc"
exit "$rc"
