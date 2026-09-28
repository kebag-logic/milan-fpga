#!/usr/bin/env bash
# Round-2 re-run of the round-1 F1 reproduction. For each variant (control, M07 board guard
# disabled, M21 call deleted inside the guard), in a disposable copy of the exact-head clone:
# elaborate the shipping AX7101 config through the builder argv (no vendor run, no firmware
# compile), count hook / interaction-report / generic MultiReg lines in the generated build
# files, then run the committed builder-bank entry test_clock_constraints.py on that copy.
# Usage: m07_elaboration_probe.sh <clean-clone> <scratch-dir> <litex-python> [config]
set -uo pipefail
SRC=$1; WORK=$2; PY=$3; CFG=${4:-endstation_ax7101_1x1_tdm8}
export PYTHONHASHSEED=0 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
export PATH="$(dirname "$PY"):/usr/bin:/bin"
for variant in control M07-board-guard-disabled M21-call-deleted-in-guard; do
  D=$WORK/elab-$variant; O=$WORK/elab-$variant-out
  rm -rf "$D" "$O"; mkdir -p "$D" "$WORK/tmp"
  (cd "$SRC" && tar --exclude=sw/builder/out -cf - .) | (cd "$D" && tar -xf -)
  "$PY" - "$D/sw/litex/milan_soc.py" "$variant" <<'PYEOF'
import sys
p, v = sys.argv[1], sys.argv[2]; t = open(p).read()
guard = '                if board == "ax7101":\n                    add_eth_constraints'
call = ('                    add_eth_constraints(platform, self.crg,\n'
        '                                        platform.lookup_request("eth_clocks", eth_phy_index).rx)')
assert t.count(guard) == 1 and t.count(call) == 1
if v.startswith("M07"):
    t = t.replace(guard, guard.replace('"ax7101"', '"ax7101-disabled"'))
elif v.startswith("M21"):
    t = t.replace(call, "                    pass")
open(p, "w").write(t)
PYEOF
  echo "== $variant ($CFG)"
  (cd "$D" && TMPDIR=$WORK/tmp "$PY" sw/builder/endstation_builder.py "configs/$CFG.yaml" >/dev/null) || { echo "builder failed"; continue; }
  ARGV=$(cd "$D" && "$PY" -c "import json;print(' '.join(json.load(open('sw/builder/out/$CFG/soc_params.json'))['argv']))")
  if (cd "$D/sw/litex" && TMPDIR=$WORK/tmp "$PY" milan_soc.py $ARGV --entity-gen-dir "$D/configs/generated/$CFG" \
        --no-compile-software --vivado-max-threads 16 --output-dir "$O" > "$WORK/elab-$variant.log" 2>&1); then
    echo "elaboration rc=0"
  else echo "elaboration FAILED"; tail -5 "$WORK/elab-$variant.log"; continue; fi
  G=$O/gateware
  echo "milan_eth_constraints lines: $(grep -c '^milan_eth_constraints' $G/alinx_ax7101.tcl)"
  echo "report_clock_interaction lines: $(grep -c report_clock_interaction $G/alinx_ax7101.tcl)"
  echo "generic MultiReg false path in XDC: $(grep -c 'filter {mr_ff == TRUE}\]$' $G/alinx_ax7101.xdc)"
  echo "order synth/hook/opt line numbers: $(grep -n -m1 '^synth_design' $G/alinx_ax7101.tcl | cut -d: -f1)/$(grep -n -m1 '^milan_eth_constraints' $G/alinx_ax7101.tcl | cut -d: -f1)/$(grep -n -m1 '^opt_design' $G/alinx_ax7101.tcl | cut -d: -f1)"
  if (cd "$D" && TMPDIR=$WORK/tmp "$PY" -B sw/builder/test_clock_constraints.py > "$WORK/elab-$variant-test.log" 2>&1); then
    echo "committed builder-bank #607 test on this tree: PASS"
  else
    echo "committed builder-bank #607 test on this tree: FAIL ($(grep -E 'AssertionError' "$WORK/elab-$variant-test.log" | tail -1 | cut -c1-100))"
  fi
  rm -rf "$D" "$O"
done
