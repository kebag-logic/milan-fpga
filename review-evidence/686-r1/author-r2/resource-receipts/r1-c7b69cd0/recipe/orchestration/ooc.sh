#!/usr/bin/env bash
# Recipe "Standalone measurements" for the two KL_pp_shadow endpoints the
# resource gate records (ooc-1x1, ooc-8x8), each with --integrated-clock.
# 1x1 binds its parameters from the integrated route's log; 8x8 from an RTL
# elaboration of its integrated script (the issue #234 method in the recipe).
set -euo pipefail
export REPO=<repo>
export WORK=<work>
export PATH="<home>/Xilinx/2026.1/Vivado/bin:$PATH"
export TMPDIR=<scratch>/tmp
LOCK=$VIVADO_LOCK
cd "$REPO"

# ---- 1x1 standalone ---------------------------------------------------------
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware" --output "$WORK/ax7101-ooc" \
  --integrated-log "$WORK/ax7101/gateware/baseline.log" --integrated-clock
(cd "$WORK/ax7101-ooc" && flock "$LOCK" vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log)

# ---- 8x8 RTL elaboration, then standalone ------------------------------------
python3 syn/ooc/pp_baseline.py "$WORK/ax8x8/gateware" --synthesis-only
mkdir -p "$WORK/ax8x8-rtl"
cp "$WORK"/ax8x8/gateware/*.xdc "$WORK"/ax8x8/gateware/*.init "$WORK/ax8x8-rtl/"
python3 - <<'PY'
import os
from pathlib import Path

work = Path(os.environ["WORK"])
lines = (work / "ax8x8/gateware/baseline_integrated.tcl").read_text().splitlines()
index = [i for i, line in enumerate(lines) if line.startswith("synth_design ")]
assert len(index) == 1, index
cut = lines[:index[0] + 1]
cut[-1] += " -rtl -rtl_skip_mlo"
(work / "ax8x8-rtl/baseline_rtl.tcl").write_text("\n".join(cut) + "\nquit\n")
PY
(cd "$WORK/ax8x8-rtl" && flock "$LOCK" vivado -mode batch -source baseline_rtl.tcl -nojournal -log baseline.log)
python3 syn/ooc/pp_baseline.py "$WORK/ax8x8/gateware" --output "$WORK/ax8x8-ooc" \
  --integrated-log "$WORK/ax8x8-rtl/baseline.log" --integrated-clock
(cd "$WORK/ax8x8-ooc" && flock "$LOCK" vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log)
