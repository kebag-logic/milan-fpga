#!/bin/sh
# Step-phase probe for the #387 gmstep leg (round R277-2).
#
# The leg's feed delay moves the accept phase against the media tick, but it
# shifts the whole event timeline with it, so the plane's step lands at the
# same phase of the listener's PDU grid at every delay. This probe adds an
# environment knob R277_STEP_SHIFT (cycles) to the GM B Sync schedule of a
# DISPOSABLE copy of sim_gmstep.cpp, builds it against the edited datapath
# (tree + the published proposed patch) through the Makefile's own
# gmstep-build recipe, runs eight shifts at feed delay 0, and restores the
# harness copy afterwards.
#
# Usage: step_shift_probe.sh <disposable clone at 021b2e07> <edited datapath> <out dir>
# Environment: VERILATOR (the pinned 5.050 wrapper), VERILATOR_JOBS.
set -eu
clone=${1:?clone}; edited=${2:?edited datapath}; out=${3:?out dir}
cd "$clone/tb/verilator/milan_dp"
mkdir -p "$out"
python3 - <<'EOF'
from pathlib import Path
p = Path("sim_gmstep.cpp")
t = p.read_text()
a = "    next_sync_ = cyc_ + kGmSyncDelayCyc;\n"
assert t.count(a) == 1
t = t.replace(a, "    next_sync_ = cyc_ + kGmSyncDelayCyc\n"
              "        + (std::getenv(\"R277_STEP_SHIFT\") ? std::stoull(std::getenv(\"R277_STEP_SHIFT\")) : 0ULL);\n")
t = t.replace("#include <algorithm>\n", "#include <algorithm>\n#include <cstdlib>\n", 1)
p.write_text(t)
EOF
trap 'git checkout -- sim_gmstep.cpp; rm -rf obj_r277_shift' EXIT
make gmstep-build GMSTEP_MDIR=obj_r277_shift DP_SRC="$edited" \
  VERILATOR="${VERILATOR:-verilator}" VERILATOR_JOBS="${VERILATOR_JOBS:-8}" > "$out/build-shift.log" 2>&1
for s in 0 40 80 119 150 190 230 249; do
  R277_STEP_SHIFT=$s ./obj_r277_shift/Vmilan_dp_gmstep obj_r277_shift/aemi.bin 0 > "$out/stepshift-s$s-d0.log" 2>&1 &
done
wait || true
for s in 0 40 80 119 150 190 230 249; do
  f="$out/stepshift-s$s-d0.log"
  echo "shift $s: $(grep -E '^== gmstep' "$f") | $(grep '^RENDER: counted recentre' "$f" | sed 's/.*(step pulse /recentre /;s/)//') | $(grep '^RESTART: mr toggle' "$f" | sed 's/.*(step pulse /mr /;s/)//')"
done
