#!/bin/sh
# Probe: after the capture has walked again, a change to a record no capture holds is refused by the running
# capture and left for the next save. Usage: probe_case4.sh <clean checkout of 81c9a1a0 with submodules> <patch>
# where <patch> is receipts/probe-case4.diff (normal diff of sw/firmware/ctrl_nvm/nvm_store.c).
# Add receipts/probe-fire-over-case4.diff on top to trap where the probe branch fires.
set -eu
tree=$1; patch_file=$2
cd "$tree"
patch sw/firmware/ctrl_nvm/nvm_store.c < "$patch_file"
python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --config configs/endstation_arty_current.yaml --jobs 16
