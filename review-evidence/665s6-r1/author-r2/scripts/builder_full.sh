#!/bin/bash
# The whole builder bank in one run, unpartitioned, on its own clean clone: LiteX from the host's venv,
# the pinned RV32 SDK under the CI HOME (as the replayed legs had it).
G=$HOME/milan-fpga-management/2026-09-23/665s6-a745b/scripts/gate.sh
export HOME=$VALIDATION_STORAGE/scratch/665s6-a745b/ci-home
export PATH=$HOME/litex-milan/venv/bin:$VALIDATION_TOOLS/verilator-v5.050/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
export LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline COURSIER_CACHE=$HOME/.cache/coursier
export SBT_OPTS="-Dsbt.offline=true -Dsbt.global.base=$HOME/.sbt -Dsbt.boot.directory=$HOME/.sbt/boot -Dsbt.ivy.home=$HOME/.ivy2"
export TMPDIR=$VALIDATION_STORAGE/scratch/665s6-a745b/builder-tmp; mkdir -p $TMPDIR
$G test-builder-require-rv32 $VALIDATION_STORAGE/scratch/665s6-a745b/builder python3 sw/builder/test_builder.py --require-rv32
