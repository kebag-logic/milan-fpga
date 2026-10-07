#!/bin/bash
# Mailbox suite (wb, axil, cosim, if2, quick mutants) on an exported copy of the exact head.
. "$(dirname "$0")/env.sh"
exec make -C $S/mbxtree/tb/verilator/mbx -j4 VERILATOR_JOBS=4 VERILATOR=${VERILATOR:-${TOOLS:-$VALIDATION_TOOLS}/pinned-verilator-5.050/verilator}
