#!/usr/bin/env bash
# Parent gates 15-16 in the scratch parent (pinned Verilator first on PATH).
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"; S="$P/scratch"
cd $S/parent
make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3; echo "GATE 15-milan_dp rc=$?"
make -C tb/verilator/milan_dp_render -j8; echo "GATE 16-milan_dp_render rc=$?"
