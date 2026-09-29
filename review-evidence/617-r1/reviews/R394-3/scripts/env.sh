# R394-3 probe environment: pinned Verilator 5.050 first on PATH, disposable temp under the packet's scratch.
# Usage: . scripts/env.sh  (from the packet root)
R394P=${R394P:-$REVIEWS/617-r394-3-packet}
export PATH=$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin:$PATH
export TMPDIR=$R394P/scratch/tmp
export VERILATOR=$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator
