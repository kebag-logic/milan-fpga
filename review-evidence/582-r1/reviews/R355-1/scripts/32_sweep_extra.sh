#!/bin/bash
# Reviewer probe of sw/litex/sweep_extra.sh --dry-run (never launches Vivado).
# Usage: 32_sweep_extra.sh <tree> <scratch-dir>
set -u
T=${1:?tree}; X=${2:?scratch}; mkdir -p "$X"
SH="$T/sw/litex/sweep_extra.sh"
clk() { grep -oE -- "--(sys|milan)-clk-freq [^ ]+" <<<"$1" | tr '\n' ' '; }
probe() { local name=$1; shift; out=$("$@" 2>&1); rc=$?; echo "[$name] rc=$rc clocks: $(clk "$out") :: $(tail -1 <<<"$out" | cut -c1-140)"; }
unset SWEEP_CFG
probe "arty default" bash "$SH" arty t --dry-run
probe "ax7101 default" bash "$SH" ax7101 t --dry-run
for c in "$T"/configs/endstation_*.yaml; do b=$(python3 -c "import yaml,sys;print(yaml.safe_load(open(sys.argv[1]))['board']['target'])" "$c")
  probe "SWEEP_CFG=$(basename "$c") board=$b" env SWEEP_CFG="configs/$(basename "$c")" bash "$SH" "$b" t --dry-run; done
probe "SWEEP_CFG absolute path" env SWEEP_CFG="$T/configs/endstation_ax7101_8x8.yaml" bash "$SH" ax7101 t --dry-run
probe "SWEEP_CFG wrong board" env SWEEP_CFG=configs/endstation_ax7101_8x8.yaml bash "$SH" arty t --dry-run
probe "SWEEP_CFG missing" env SWEEP_CFG=configs/does_not_exist.yaml bash "$SH" ax7101 t --dry-run
probe "SWEEP_CFG empty (falls to default)" env SWEEP_CFG= bash "$SH" ax7101 t --dry-run
# A variant config at a non-contract clock must be refused by the builder load.
python3 - "$T" "$X/variant.yaml" <<'PY'
import sys, yaml
raw = yaml.safe_load(open(sys.argv[1] + "/configs/endstation_ax7101_1x1_tdm8.yaml"))
raw["board"]["constraints"]["milan_clk_hz"] = 100_000_000
open(sys.argv[2], "w").write(yaml.safe_dump(raw))
PY
probe "SWEEP_CFG 100 MHz variant" env SWEEP_CFG="$X/variant.yaml" bash "$SH" ax7101 t --dry-run
probe "unknown board" bash "$SH" zynq t --dry-run
# Run from another working directory: the script resolves the repository itself.
probe "cwd=/ default ax7101" bash -c "cd / && bash '$SH' ax7101 t --dry-run"
