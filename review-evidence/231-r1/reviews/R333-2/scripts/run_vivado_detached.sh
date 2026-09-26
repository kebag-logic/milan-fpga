#!/usr/bin/env bash
# Launch one Vivado batch run detached (session tool calls are capped at 10 min);
# the caller polls for <dir>/run_rc.txt in foreground calls.
# Usage: run_vivado_detached.sh <dir> <tcl> [tclargs...]
set -euo pipefail
dir="$1"; tcl="$2"; shift 2
cd "$dir"
rm -f run_rc.txt
setsid nohup bash -c 'export PATH=${VIVADO_BIN:?set VIVADO_BIN to the Vivado 2026.1 bin directory}:$PATH; vivado -mode batch -source "$0" -nojournal -log baseline.log ${1:+-tclargs "$@"} > vivado_stdout.txt 2>&1; echo $? > run_rc.txt' "$tcl" "$@" < /dev/null > /dev/null 2>&1 &
echo "launched pid $!"
