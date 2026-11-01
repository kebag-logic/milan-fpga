#!/bin/bash
# Make a disposable source copy for one gptp_txts probe: mk_probe.sh <dir>
# Arguments: destination directory. HEADSRC names the exact-head export.
set -e
d=$1; src=${HEADSRC:?}
mkdir -p "$d/tb/verilator" "$d/third_party" "$d/sw"
cp -a "$src/hdl" "$d/hdl"
cp -a "$src/tb/common" "$d/tb/common"
cp -a "$src/tb/verilator/gptp_txts" "$d/tb/verilator/gptp_txts"
cp -a "$src/sw/litex" "$d/sw/litex"
ln -s "$src/gptp-processor" "$d/gptp-processor"
ln -s "$src/third_party/verilog-axis" "$d/third_party/verilog-axis"
