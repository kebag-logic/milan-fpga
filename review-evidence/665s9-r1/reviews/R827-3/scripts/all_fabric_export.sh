#!/usr/bin/env bash
# all_fabric_export.sh TREE CONFIG_STEM OUT LITEX_PY: the all-fabric SoC export
# (no Vivado, no software compile) of one shipped config from one checkout.
# The builder writes its artifacts under OUT.builder, never into the checkout.
set -euo pipefail
tree=$(cd "$1" && pwd); stem=$2; out=$3; py=$4
mkdir -p "$out.builder"
cd "$tree/sw/builder"
argv=$("$py" -c "
import contextlib, io, sys, endstation_builder as eb
p='../../configs/$stem.yaml'
with contextlib.redirect_stdout(io.StringIO()): eb.build(p, sys.argv[1])
print(' '.join(eb.emit_soc_argv(eb.load_config(p))))" "$out.builder")
cd "$tree/sw/litex"
echo "tree=$tree head=$(git -C "$tree" rev-parse HEAD) argv=$argv" > "$out.argv"
# shellcheck disable=SC2086
PYTHONHASHSEED=0 "$py" milan_soc.py $argv --entity-gen-dir "$tree/configs/generated/$stem" \
  --no-compile-software --output-dir "$out" > "$out.log" 2>&1
