#!/usr/bin/env bash
# R324-3: run scripts/check_nvm_capture.py with PATH holding only python3 and
# git, a clean environment (no PYTHONPATH), and report whether LiteX/migen or
# any compiler/simulator is reachable. Usage: CLONE=<clone> bash gate_minimal_env.sh
set -uo pipefail
PKT=$(cd "$(dirname "$0")" && pwd); : "${CLONE:?set CLONE}"
D=$PKT/scratch/minbin; mkdir -p "$D"
ln -sf "$(command -v python3)" "$D/python3"; ln -sf "$(command -v git)" "$D/git"
cd "$CLONE"
echo "PATH=<packet>/scratch/minbin (python3, git only)"
env -i HOME="$HOME" PATH="$D" PYTHONDONTWRITEBYTECODE=1 python3 -c 'import importlib.util as u; print("litex importable:", u.find_spec("litex") is not None, "migen importable:", u.find_spec("migen") is not None)'
env -i HOME="$HOME" PATH="$D" PYTHONDONTWRITEBYTECODE=1 python3 -c 'import shutil; print("compilers:", [c for c in ("gcc","cc","g++","riscv32-linux-gcc","riscv64-unknown-elf-gcc","verilator","iverilog") if shutil.which(c)])'
env -i HOME="$HOME" PATH="$D" PYTHONDONTWRITEBYTECODE=1 python3 -X importtime scripts/check_nvm_capture.py 2> "$D/importtime.log"; echo "gate rc=$?"
echo "litex/migen/verilator modules imported: $(grep -cE '\| +(litex|migen|litedram)' "$D/importtime.log")"
