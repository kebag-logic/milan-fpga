#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Prepare the disposable probe area for this packet from a clean clone at the
# exact head (submodules protocol-processor, gptp-processor and
# third_party/verilog-axis initialised at their gitlinks):
#   scratch/tree        byte copy of the clone without .git
#   scratch/srcs.txt    milan_dp `make -s print-srcs` (relative paths)
#   scratch/dpvflags.txt milan_dp `make -s print-dp-vflags`
#   scratch/mutants/    the single-edit datapath copies (make_mutants.py)
# Python runs with bytecode writing disabled so the clone gains no residue.
#
# usage: setup_scratch.sh <clone>
set -euo pipefail
clone=$(readlink -f "$1")
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
S=$PACKET/scratch
mkdir -p "$S/tree"
(cd "$clone" && tar --exclude=.git -cf - .) | tar -xf - -C "$S/tree"
export PYTHONDONTWRITEBYTECODE=1
make -s -C "$clone/tb/verilator/milan_dp" print-srcs > "$S/srcs.txt"
make -s -C "$clone/tb/verilator/milan_dp" print-dp-vflags > "$S/dpvflags.txt"
python3 -B "$PACKET/scripts/make_mutants.py" \
  "$S/tree/hdl/milan/milan_datapath.sv" "$S/mutants"
git -C "$clone" status --porcelain --ignored --ignore-submodules=none
