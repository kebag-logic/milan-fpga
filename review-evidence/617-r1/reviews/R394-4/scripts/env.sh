# R394-4 probe environment: pinned Verilator 5.050 first on PATH, disposable temp under the packet's scratch.
# Usage: . scripts/env.sh  (from the packet root). MAKE43=1 puts the scratch-built GNU make 4.3 first.
R394P=${R394P:-$REVIEWS/617-r394-4-packet}
export PATH=$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin:$PATH
[ -n "$MAKE43" ] && export PATH=$R394P/scratch/make43/inst/bin:$PATH
export TMPDIR=$R394P/scratch/tmp
export VERILATOR=$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator
