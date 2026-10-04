#!/bin/sh
# Run the committed tb/pp_top/acmp_mutants.py of a tree unchanged, with its
# temporary extracts under the packet's scratch (TMPDIR) rather than the shared
# /tmp. Usage: campaign.sh TREE OUTPUT VERILATOR JOBS
set -eu
export TMPDIR=$(dirname "$2")/tmp CAMP="$1/tb/pp_top/acmp_mutants.py" CAMPARGS="--output $2 --verilator $3 --jobs $4"
mkdir -p "$TMPDIR"
cd "$1"
exec python3 -c 'import os, runpy, sys; p = os.environ["CAMP"]; sys.argv = [p] + os.environ["CAMPARGS"].split(); runpy.run_path(p, run_name="__main__")'
