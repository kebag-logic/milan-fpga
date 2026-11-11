#!/usr/bin/env bash
# endpoint_export.sh TREE CONFIG_STEM OUT: the all-fabric export of one shipped config from one tree
set -euo pipefail
tree=$1; stem=$2; out=$3
py=<home>/litex-milan/venv/bin/python3
cd "$tree/sw/builder"
argv=$("$py" -c "
import contextlib, io, endstation_builder as eb
p='../../configs/$stem.yaml'
with contextlib.redirect_stdout(io.StringIO()): eb.build(p)
print(' '.join(eb.emit_soc_argv(eb.load_config(p))))")
cd "$tree/sw/litex"
# shellcheck disable=SC2086
PYTHONHASHSEED=0 "$py" milan_soc.py $argv --entity-gen-dir "$tree/configs/generated/$stem" ${FLOW:-} --no-compile-software --output-dir "$out" > "$out.log" 2>&1
