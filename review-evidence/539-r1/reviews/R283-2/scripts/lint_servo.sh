#!/bin/sh
# Focused -Wall lint of KL_mmcm_drp_servo (default parameters) in one source tree.
# usage: VERILATOR=<pinned wrapper> lint_servo.sh <src-tree>; prints warnings, exit = verilator's
set -u
S=$1
cd "$S" && "${VERILATOR:?}" --lint-only -Wall --top-module KL_mmcm_drp_servo \
  hdl/common/cdc_pulse.sv hdl/common/cdc_handshake.sv hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 2>&1
