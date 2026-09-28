#!/usr/bin/env bash
# Build a pins-only LiteX environment the way elaborate.yml does, isolated HOME.
# Usage: setup_pins_env.sh <clone> <packet>
set -euo pipefail
CLONE=$1; PKT=$2; S=$PKT/scratch
export HOME=$S/pinshome
export PATH="$S/pins-venv/bin:$S/bin:/usr/bin:/bin"
cd "$CLONE"
python3 --version
python3 -m pip install --quiet pyyaml
python3 -m pip install --quiet -r sw/litex/litex_pins.txt
python3 scripts/ci_litex_env.py
PYTHON=python3 sw/litex/patches/apply.sh
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
python3 -m pip freeze > "$PKT/receipts/11_pins_env_freeze.txt"
python3 -c 'import importlib.util as u; print("picolibc:", u.find_spec("pythondata_software_picolibc")); print("compiler_rt:", u.find_spec("pythondata_software_compiler_rt"))'
