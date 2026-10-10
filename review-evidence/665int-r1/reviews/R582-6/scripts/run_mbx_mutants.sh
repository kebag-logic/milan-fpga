#!/bin/sh
# Run the mailbox bench's full planted-defect table in a disposable clone with the pinned Verilator.
# Usage: run_mbx_mutants.sh CLONE VERILATOR LOG RC
cd "$1/tb/verilator/mbx" || exit 2
VERILATOR="$2" python3 -B mutants.py --jobs 8 > "$3" 2>&1
echo $? > "$4"
