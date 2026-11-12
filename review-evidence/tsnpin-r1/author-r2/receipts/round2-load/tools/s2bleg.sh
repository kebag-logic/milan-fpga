#!/usr/bin/env bash
# s2bleg.sh <tree> <point> <build-dir>: S2b's budget harness at one point, its default groups, as S2b's legs ran it, on the pinned RV32 SDK.
set -u
T=$1; P=$2; B=$3
S=<pinned-rv32-sdk>
export MILAN_RV32_CC=$S/bin/riscv32-linux-gcc
export PATH=<litex-env>/venv/bin:$S/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<tools-scratch>/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tools>/pinned-verilator-5.050/verilator LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONUNBUFFERED=1
export TMPDIR=<scratch>/tmp MAKEFLAGS="-j8 --no-print-directory"
cd "$T" || exit 3
echo "HEAD $(git rev-parse HEAD) tsn-c-stack $(git -C third_party/tsn-c-stack rev-parse HEAD) acmp delta $(git diff --cached --stat -- sw/firmware/ctrl/acmp | tail -1)"
python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$B" --record-budget-findings --record-share-findings --jobs 4
