#!/usr/bin/env bash
# R324-1 probe setup: build the isolated scratch tree used by probe_step.py.
# Usage: CLONE=<exact-head clone> SDK_BIN=... VERILATOR_BIN=... bash probe_setup.sh
set -euo pipefail
PKT=$(cd "$(dirname "$0")" && pwd)
: "${CLONE:?set CLONE to the exact-head review clone}"
LITEX_ENV_DIR=${LITEX_ENV_DIR:-$HOME/litex-milan}
E=$PKT/scratch/env
mkdir -p "$E"
for d in litex litedram litespi liteeth pythondata-software-picolibc pythondata-software-compiler_rt; do
  cp -a "$LITEX_ENV_DIR/$d" "$E/"
done
O=$E/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv
mkdir -p "$O/verilog"
cp "$LITEX_ENV_DIR/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/__init__.py" "$O/"
for f in "$LITEX_ENV_DIR"/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/*; do
  [ -f "$f" ] && ln -s "$f" "$O/verilog/"
done
# Three repository copies: the unmodified head (control), the 50 MHz CPU
# variant, and the 50 MHz variant with PLL-aligned edges.
cp -a "$CLONE" "$PKT/scratch/repo_head"
cp -a "$CLONE" "$PKT/scratch/repo"
(cd "$PKT/scratch/repo" && git apply "$PKT/receipts/probes/probe_edit_50mhz.patch")
cp -a "$CLONE" "$PKT/scratch/repo_phase"
(cd "$PKT/scratch/repo_phase" && git apply "$PKT/receipts/probes/probe_edits_50mhz_phase.patch")
echo "setup done under $PKT/scratch"
# Then, per arm (repo copy, shape endstation_ax7101_8x8, --captures 2):
#   . probe_env.sh; cd scratch/<copy>
#   python3 ../../probe_step.py elaborate --shape endstation_ax7101_8x8 --captures 2 [--mutation no-traffic] --build-dir ../<arm>
#   python3 ../../probe_step.py verilate --build-dir ../<arm>
#   python3 ../../probe_step.py make --build-dir ../<arm>
#   python3 ../../probe_step.py simulate --build-dir ../<arm>
# Arms: b8x8_100 (repo_head), b8x8_100_nt (repo_head, no-traffic),
#       b8x8_50 (repo), b8x8_50_nt (repo, no-traffic), b8x8_50_phase (repo_phase).
