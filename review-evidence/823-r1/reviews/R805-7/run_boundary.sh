#!/bin/sh
# The TSN stack boundary gate (the ctrl_configs.py reader) at a candidate tree; argv: TREE RECEIPTS_DIR PYTHONPATH.
# Needs MILAN_RV32_CC; PYTHONPATH holds the LiteX packages at sw/litex/litex_pins.txt's revisions.
T=$1; R=$2; cd "$T" || exit 2
PYTHONPATH=$3 python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator > "$R/ctrl_boundary.log" 2>&1; echo $? > "$R/ctrl_boundary.rc"
