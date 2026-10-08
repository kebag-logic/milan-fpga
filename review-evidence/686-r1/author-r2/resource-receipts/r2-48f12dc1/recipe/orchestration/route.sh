#!/usr/bin/env bash
# Recipe "Integrated measurements", 1x1 shipping route (ExtraPostPlacementOpt),
# docs/testing/PP_SHADOW_BASELINE_RECIPE.md. Vivado only under the shared lock.
set -euo pipefail
export REPO=<repo>
export WORK=<work>
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$PATH"
export TMPDIR=<scratch>/tmp
cd "$REPO"
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware" --single-thread-synthesis
cd "$WORK/ax7101/gateware"
flock $VIVADO_LOCK bash -c \
  'date -Is > route.start; vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log; rc=$?; date -Is > route.end; exit $rc'
