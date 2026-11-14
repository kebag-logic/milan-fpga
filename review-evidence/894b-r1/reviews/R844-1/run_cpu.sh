#!/usr/bin/env bash
# Existing configured compiler and simulator must be on PATH; no installs or generation of shared tools.
set -eu
checkout=$(realpath "$1")
scratch=$(realpath "$2")
soc_python=$3
packet=$(cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$scratch/guard"
cp "$packet/safe_build_guard.py" "$scratch/guard/sitecustomize.py"
export REVIEW_SCRATCH="$scratch" TMPDIR="$scratch" PYTHONPATH="$scratch/guard"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
cd "$checkout"
verilator --version
"$soc_python" -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if \
  --build-dir "$scratch/cpu-build" --variant answering-every-port \
  --groups notice-burst-0,notice-burst-3 --jobs 8 \
  --record-budget-findings --record-share-findings
