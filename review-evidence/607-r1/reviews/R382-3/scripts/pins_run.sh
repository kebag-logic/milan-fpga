#!/usr/bin/env bash
# Run a command inside the pins-only elaborate environment built by build_pins_env.sh.
# HOME is private (the pinned RV32 SDK lives at $HOME/br-milan-rv32/host, as in CI),
# python3 is the pins-only venv, sv2v is the pinned v0.0.12, and PATH is rebuilt from
# /usr/bin without tools the hosted elaborate step does not have at that point
# (Verilator is installed only after the bank step; no cross compiler, Yosys or
# Icarus is installed by the job). No bench venv is reachable: the bank's sweep.sh
# fallback resolves under the private HOME, where no litex-milan venv exists.
# Usage: pins_run.sh <tree> <command...>
set -uo pipefail
PKT=${PKT:?set PKT to the packet directory}
S="$PKT/scratch"
TREE=$1; shift
if [ ! -d "$S/sysbin" ]; then
  mkdir -p "$S/sysbin"
  for f in /usr/bin/* /bin/*; do
    b=$(basename "$f")
    case "$b" in verilator*|yosys*|riscv*|iverilog*|vvp*|python3*|python) continue ;; esac
    [ -e "$S/sysbin/$b" ] || ln -s "$f" "$S/sysbin/$b"
  done
fi
export HOME="$S/home"
export PATH="$S/bin:$S/pins-venv/bin:$S/sysbin"
unset MILAN_LITEX_PYTHON PYTHONPATH VIRTUAL_ENV
cd "$TREE"
exec "$@"
