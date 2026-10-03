#!/usr/bin/env bash
# Parent gates 12-14 in the scratch parent (pinned Verilator first on PATH).
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"; S="$P/scratch"; V="$S/bin/verilator"
cd $S/parent
make -C tb/verilator/pp_shadow -j8; echo "GATE 12-pp_shadow rc=$?"
make -C tb/verilator/nvm_cosim lint; echo "GATE 13-nvm_cosim-lint rc=$?"
make -C tb/verilator/nvm_cosim quick; echo "GATE 14-nvm_cosim-quick rc=$?"
