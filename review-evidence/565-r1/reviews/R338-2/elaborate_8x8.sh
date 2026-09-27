#!/bin/bash
# Gateware export (no vendor tools, no software compile) of the 8x8 shape at the
# checked-out revision of <repo>. Usage: elaborate_8x8.sh <repo> <litex-venv-python> <out-dir>
set -eu
repo=$1 py=$2 out=$3
cd "$repo"
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
python3 -B sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml > /dev/null
argv=$(python3 -c "import json;print(' '.join(json.load(open('sw/builder/out/endstation_ax7101_8x8/soc_params.json'))['argv']))")
echo "REV $(git rev-parse HEAD)"; echo "ARGV $argv"
# shellcheck disable=SC2086
unshare -Urn "$py" -B sw/litex/milan_soc.py $argv --entity-gen-dir "$repo/configs/generated/endstation_ax7101_8x8" \
  --output-dir "$out" --no-compile-software
