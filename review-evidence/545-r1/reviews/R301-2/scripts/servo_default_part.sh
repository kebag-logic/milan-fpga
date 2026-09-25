#!/usr/bin/env bash
# The default mmcm_servo `run` recipe at the head, split into the Makefile's
# own sequential steps so each fits one foreground command; every step is
# pinned to the same two CPUs and timed. Sum of the parts = default wall.
#   build : clean, unit-build, unit run, rails build+run, phc_step_build
#   step  : ./obj_phc/Vphc_step           (#539 step suite)
#   slew  : ./obj_phc/Vphc_step +slew_suite (#545 slew suite)
set -u
PKT=${PKT:-$REVIEWS/545-r301-2-packet}
VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
CPUS=${CPUS:-8,9}
D="$PKT/scratch/tree/tb/verilator/mmcm_servo"
cd "$D" || exit 2
s=$(date +%s.%N)
case "$1" in
  build)
    make -s clean
    taskset -c "$CPUS" make unit-build VERILATOR="$VERILATOR" && taskset -c "$CPUS" ./obj_dir/Vservo_sim &&
    taskset -c "$CPUS" "$VERILATOR" --cc --exe --build -j 0 -Wall -Wno-fatal -Werror-UNDRIVEN \
      -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
      -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
      --top-module rails_wrap -Mdir obj_rails ../../../hdl/common/cdc_pulse.sv \
      ../../../hdl/common/cdc_handshake.sv ../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv \
      ../../../hdl/common/cdc_pair_fifo.sv ../../../hdl/ieee1722/aaf/KL_i2s_playback.sv \
      rails_wrap.sv sim_rails.cpp -o Vrails_sim >/dev/null &&
    taskset -c "$CPUS" ./obj_rails/Vrails_sim &&
    taskset -c "$CPUS" make --no-print-directory phc_step_build VERILATOR="$VERILATOR" >/dev/null
    rc=$? ;;
  step) taskset -c "$CPUS" ./obj_phc/Vphc_step; rc=$? ;;
  slew) taskset -c "$CPUS" ./obj_phc/Vphc_step +slew_suite; rc=$? ;;
  *) echo "usage: $0 build|step|slew"; exit 2 ;;
esac
e=$(date +%s.%N)
echo "PART $1 rc=$rc wall_s=$(echo "$e - $s" | bc) cpus=$CPUS"
exit $rc
