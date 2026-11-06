#!/usr/bin/env bash
# One enforced service plan at the reviewed head, in a disposable copy.
# Usage: svc_probe.sh <repo-copy> <scratch> <shape> <plan> <tag> <receipts>
set -u
repo=$1; scratch=$2; shape=$3; plan=$4; tag=$5; rec=$6
# Set PRODUCT_PYTHON, SDK_BIN and SIM_BIN for the local product environment.
: "${PRODUCT_PYTHON:?}" "${SDK_BIN:?}" "${SIM_BIN:?}"
export PYTHON="$PRODUCT_PYTHON" LITEX_ENV_CC_TRIPLE=riscv32-linux
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PATH="$SIM_BIN:/usr/local/bin:/usr/bin:/bin:$(dirname "$PRODUCT_PYTHON"):$SDK_BIN"
export TMPDIR="$scratch/tmp"; mkdir -p "$TMPDIR"
cd "$repo" || exit 2
verilator --version > "$rec/svc-$tag.tools" 2>&1
date -Is > "$rec/svc-$tag.start"
"$PRODUCT_PYTHON" -B tb/verilator/fw_service_budget/run.py --shape "$shape" --build-dir "$scratch/fw-$tag" --build-only > "$rec/svc-$tag-build.log" 2>&1
echo $? > "$rec/svc-$tag-build.rc"
"$PRODUCT_PYTHON" -B tb/verilator/fw_service_budget/run.py --shape "$shape" --build-dir "$scratch/fw-$tag" --reuse-build --populated --plan "$plan" --enforce-service > "$scratch/run-$tag.log" 2>&1
echo $? > "$rec/svc-$tag.rc"
date -Is > "$rec/svc-$tag.end"
