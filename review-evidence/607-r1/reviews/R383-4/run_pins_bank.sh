#!/usr/bin/env bash
# Builder bank in the pins-only environment (as elaborate.yml): isolated HOME, no MILAN_LITEX_PYTHON.
# Usage: run_pins_bank.sh <clone> <packet>
set -u
CLONE=$1; PKT=$2; S=$PKT/scratch
export HOME=$S/pinshome
export PATH="$S/pins-venv/bin:$S/bin:/usr/bin:/bin"
unset MILAN_LITEX_PYTHON
cd "$CLONE"
{ command -v python3; python3 --version; sv2v --version; verilator --version; } > "$PKT/receipts/12_pins_bank_env.txt" 2>&1
python3 -c 'import importlib.util as u; print("picolibc", u.find_spec("pythondata_software_picolibc")); print("compiler_rt", u.find_spec("pythondata_software_compiler_rt"))' >> "$PKT/receipts/12_pins_bank_env.txt" 2>&1
start=$(date +%s)
python3 sw/builder/test_builder.py --require-elaboration --require-rv32 > "$PKT/receipts/12_pins_bank.log" 2>&1
rc=$?
echo "rc=$rc seconds=$(( $(date +%s) - start )) head=$(git rev-parse HEAD)" > "$PKT/receipts/12_pins_bank.rc"
