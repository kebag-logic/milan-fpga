#!/bin/bash
# Reviewer probe (#911): elaborate one build.sh recipe (no Vivado, no --build)
# from the clone at $1 into $3, using the argv build.sh --dry-run prints.
# usage: elaborate.sh <clone> <recipe> <output dir> <venv bin>
set -euo pipefail
clone=$1 recipe=$2 out=$3 venv=$4
export PATH="$venv:$PATH"
cd "$clone"
line=$(bash sw/litex/build.sh "$recipe" --dry-run 2>/dev/null | grep -m1 'exec python3 milan_soc.py')
argv=${line#*exec python3 milan_soc.py }
argv=${argv% --build --output-dir *}
mkdir -p "$out"
cd "$clone/sw/litex"
export PYTHONHASHSEED=0
# shellcheck disable=SC2086  # argv is build.sh's word list, split as build.sh splits it
exec python3 milan_soc.py $argv --output-dir "$out"
