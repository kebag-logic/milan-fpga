#!/usr/bin/env bash
# R324-3 probe setup: isolated scratch copies of the LiteX packages, a symlink
# overlay of the CPU netlist cache (a missing netlist fails instead of being
# generated into a shared install) and a copy of the exact-head clone.
# Usage: CLONE=<exact-head clone> bash probe_setup.sh
set -euo pipefail
PKT=$(cd "$(dirname "$0")" && pwd)
: "${CLONE:?set CLONE to the exact-head review clone}"
LITEX_ENV_DIR=${LITEX_ENV_DIR:-$HOME/litex-milan}
E=$PKT/scratch/env
mkdir -p "$E"
for d in litex migen litedram litespi liteeth pythondata-software-picolibc pythondata-software-compiler_rt; do
  cp -a "$LITEX_ENV_DIR/$d" "$E/"
done
O=$E/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv
mkdir -p "$O/verilog"
cp "$LITEX_ENV_DIR/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/__init__.py" "$O/"
for f in "$LITEX_ENV_DIR"/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/*; do
  [ -f "$f" ] && ln -s "$f" "$O/verilog/"
done
cp -a "$CLONE" "$PKT/scratch/repo_head"
# Independent clock route (round-1 method): the 8x8 yaml edited to 50 MHz.
cp -a "$CLONE" "$PKT/scratch/repo_yaml"
(cd "$PKT/scratch/repo_yaml" && git apply "$PKT/probe_edit_50mhz.patch")
echo "setup done under $PKT/scratch"
