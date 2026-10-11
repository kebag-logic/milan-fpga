#!/usr/bin/env bash
# Run a command in the product build environment the capture receipt records
# (the product LiteX venv, the pinned RV32 SDK compiler, offline, fixed hash
# seed), from the repository root, in a network namespace.
# Usage: product_env.sh <repo> <scratch-tmp> <command>...
set -u
repo=$1; scratch=$2; shift 2
export PRODUCT_PYTHON="$HOME/litex-milan/venv/bin/python"
export PYTHON="$PRODUCT_PYTHON"
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
export PATH="$HOME/litex-milan/venv/bin:/usr/local/bin:/usr/bin:/bin:$HOME/br-milan-rv32/host/bin"
export TMPDIR="$scratch"
mkdir -p "$TMPDIR"
cd "$repo" || exit 2
exec unshare -Urn "$@"
