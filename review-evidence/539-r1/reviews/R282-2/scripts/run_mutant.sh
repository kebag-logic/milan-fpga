#!/bin/sh
# One mutant: export head, mutate the servo, build and run the unit harness
# (sim_main.cpp) and the silicon-scale step harness (sim_phc_step.cpp), -j 1.
set -u
. "$(dirname "$0")/env.sh"
M="$1"
W="$PKT/scratch/mut/$M"
rm -rf "$W"; mkdir -p "$W"
git -C "$CLONE" archive "$HEAD_SHA" hdl tb/common tb/verilator/mmcm_servo | tar -x -C "$W"
python3 "$PKT/scripts/mutate.py" "$M" "$W/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv" || exit 2
git -C "$CLONE" show "$HEAD_SHA:hdl/ieee1722/crf/KL_mmcm_drp_servo.sv" | diff - "$W/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
VF=$(printf '%s' "$VFLAGS_R" | sed 's/-j 8/-j 1/')
D="$W/tb/verilator/mmcm_servo"
cd "$D"
eval "$VERILATOR $VF --top-module KL_mmcm_drp_servo -GTICK_CYC_P=3072 -GWIN_LOG2_P=5 \"-GNOM_WIN_NS_P=64'd4000000\" -GNORM_SHIFT_P=7 -GGAIN_NUM_P=7 -GRELOCK_TOUT_P=20000 -GLOCK_THR_P=8192 ../../../hdl/common/cdc_pulse.sv ../../../hdl/common/cdc_handshake.sv ../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv sim_main.cpp -o Vservo_sim" > build_unit.log 2>&1 || { echo "UNIT BUILD FAILED"; tail -20 build_unit.log; }
eval "$VERILATOR $VF --public-flat-rw --top-module KL_mmcm_drp_servo -Mdir obj_phc ../../../hdl/common/cdc_pulse.sv ../../../hdl/common/cdc_handshake.sv ../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv sim_phc_step.cpp -o Vphc_step" > build_phc.log 2>&1 || { echo "PHC BUILD FAILED"; tail -20 build_phc.log; }
echo "=== unit"; ./obj_dir/Vservo_sim; echo "unit exit=$?"
echo "=== phc_step"; ./obj_phc/Vphc_step; echo "phc exit=$?"
