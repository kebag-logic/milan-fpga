#!/usr/bin/env bash
export TMPDIR=/data-2/milan/tmp/opt-a837-r2/tmp
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
export GIT_ALLOW_PROTOCOL=file:https
export MAKEFLAGS='-j4 --no-print-directory'
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4 CI_CENSUS_JOBS=2
mkdir -p "$TMPDIR"
