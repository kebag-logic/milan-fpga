#!/usr/bin/env bash
# Review probes for PR #770 at f1fda3f1 (reproduction recipe).
#
# Usage: run_probes.sh <clean checkout of f1fda3f1> <work dir>
# Needs a Verilator 5.050 as $VERILATOR (default: verilator on PATH).
#
# 1. Copies tb/verilator/media_phase to <checkout>/tb/verilator/media_phase_probe
#    inside a COPY of the checkout, applies sim_main_phcstep.patch (two extra
#    cases: an instantaneous local PHC step of +20,000 ns and of +7,000 ns, no
#    slew level, each graded with the suite's own re-acquisition, hold and
#    let-go checks) and Makefile_cases.patch.
# 2. Builds the clean probe harness and one per servo patch:
#      p1 servo_p1_no_step_hold.patch   ptp_jump_r left out of the phase hold
#      p2 servo_p2_settled_always.patch ph_settled_o = engaged (band and count ignored)
#      p3 servo_p3_no_range.patch       the +/-2^25 ns fold-range guard removed
# 3. Runs the suite's ten cases on p1, p2, p3 and the two PHC step cases on
#    clean and p1. Each case writes out/<build>.<case>.log and .rc.
set -euo pipefail
src=$(cd "$1" && pwd)
work=$(mkdir -p "$2" && cd "$2" && pwd)
here=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-verilator}
cp -a "$src" "$work/src"
d="$work/src/tb/verilator/media_phase_probe"
cp -a "$work/src/tb/verilator/media_phase" "$d"
(cd "$d" && patch -p4 < "$here/probes/sim_main_phcstep.patch" && patch -p4 < "$here/probes/Makefile_cases.patch")
servo="$work/src/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
for p in p1:servo_p1_no_step_hold p2:servo_p2_settled_always p3:servo_p3_no_range; do
  tag=${p%%:*}; name=${p#*:}
  cp "$servo" "$work/$name.sv"
  patch "$work/$name.sv" < "$here/probes/$name.patch"
  make -C "$d" VERILATOR="$V" MDIR="obj_$tag" SERVO_RTL="$work/$name.sv" build
done
make -C "$d" VERILATOR="$V" MDIR=obj_clean build
mkdir -p "$d/out"
{
  for c in engage engage2 step ramp holdover internal mr slew burst carry; do
    echo "obj_p1 $c"; echo "obj_p2 $c"; echo "obj_p3 $c"
  done
  for b in obj_clean obj_p1; do echo "$b phcstep"; echo "$b phcstep7"; done
} > "$d/jobs.txt"
cd "$d"
xargs -P "${JOBS:-8}" -L 1 sh -c './$0/Vmedia_phase +case=$1 > out/$0.$1.log 2>&1; echo $? > out/$0.$1.rc' < jobs.txt
grep -H . out/*.rc
