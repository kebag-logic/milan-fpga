#!/usr/bin/env bash
# Reproduce finding F1: in a disposable copy of the exact-head clone, stop the real
# MilanSoC from calling add_eth_constraints for the AX7101, elaborate the shipping
# 1x1 TDM8 recipe without Vivado, and show the generated build silently regresses.
# Usage: m07_elaboration_probe.sh <clean-clone> <scratch-dir> <litex-python> <rv32-sdk-bin-dir>
set -euo pipefail
SRC=$1; WORK=$2; PY=$3; SDK=$4; D=$WORK/m07-elab
rm -rf "$D" "$WORK/m07-out"; mkdir -p "$D"
(cd "$SRC" && tar --exclude=sw/builder/out -cf - .) | (cd "$D" && tar -xf -)
"$PY" - "$D/sw/litex/milan_soc.py" <<'PYEOF'
import sys
p = sys.argv[1]; t = open(p).read()
old = '                if board == "ax7101":\n                    add_eth_constraints'
assert t.count(old) == 1
open(p, "w").write(t.replace(old, old.replace('"ax7101"', '"ax7101-disabled"')))
PYEOF
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$WORK
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
export PATH="$(dirname "$PY"):/usr/bin:$SDK:$PATH"
cd "$D" && "$PY" sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml >/dev/null
ARGV=$("$PY" -c "import json;print(' '.join(json.load(open('sw/builder/out/endstation_ax7101_1x1_tdm8/soc_params.json'))['argv']))")
(cd sw/litex && "$PY" milan_soc.py $ARGV --entity-gen-dir "$D/configs/generated/endstation_ax7101_1x1_tdm8" \
   --vivado-max-threads 16 --output-dir "$WORK/m07-out" > "$WORK/m07-elab.log" 2>&1) && echo "elaboration rc=0" || { tail -5 "$WORK/m07-elab.log"; exit 1; }
G=$WORK/m07-out/gateware
echo "milan_eth_constraints lines: $(grep -c milan_eth_constraints $G/alinx_ax7101.tcl || true)"
echo "report_clock_interaction lines: $(grep -c report_clock_interaction $G/alinx_ax7101.tcl || true)"
echo "generic MultiReg false path in XDC: $(grep -c 'filter {mr_ff == TRUE}\]$' $G/alinx_ax7101.xdc || true)"
(cd "$D" && "$PY" -B sw/builder/test_clock_constraints.py >/dev/null 2>&1) && echo "committed #607 test on the mutant: PASS (mutant survives)"
rm -rf "$D" "$WORK/m07-out"
