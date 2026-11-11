#!/usr/bin/env bash
# s2.sh <tree> <point> <build-dir> <jobs>: S2's CPU budget harness at one point, as its README runs it.
set -u
T=$1; P=$2; B=$3; J=$4
export PATH=<rv32-sdk>/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export VERILATOR=<tools>/pinned-verilator-5.050/verilator TMPDIR=<scratch>/tmp
cd "$T" || exit 3
git -C "$T" submodule status third_party/tsn-c-stack
<litex-env>/venv/bin/python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$B" --record-budget-findings --jobs "$J" ${S2_GROUPS:+--groups "$S2_GROUPS"}
