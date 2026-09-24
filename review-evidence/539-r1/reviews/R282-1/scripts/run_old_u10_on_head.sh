#!/bin/sh
# The BASE unit harness (old single-sample U10 trim check) against the HEAD RTL,
# to see what the U10 envelope change replaced.
set -u
. "$(dirname "$0")/env.sh"
W="$PKT/scratch/old_u10"
rm -rf "$W"; mkdir -p "$W"
git -C "$CLONE" archive "$HEAD_SHA" hdl tb/common | tar -x -C "$W"
git -C "$CLONE" archive "$BASE_SHA" tb/verilator/mmcm_servo | tar -x -C "$W"
cd "$W/tb/verilator/mmcm_servo"
VF=$(printf '%s' "$VFLAGS_R" | sed 's/-j 8/-j 2/')
eval "$VERILATOR $VF --top-module KL_mmcm_drp_servo -GTICK_CYC_P=3072 -GWIN_LOG2_P=5 \"-GNOM_WIN_NS_P=64'd4000000\" -GNORM_SHIFT_P=7 -GGAIN_NUM_P=7 -GRELOCK_TOUT_P=20000 -GLOCK_THR_P=8192 ../../../hdl/common/cdc_pulse.sv ../../../hdl/common/cdc_handshake.sv ../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv sim_main.cpp -o Vservo_sim" > build.log 2>&1 || echo BUILD FAILED
./obj_dir/Vservo_sim | grep -E "U10|FAIL|checks"; echo "old harness on head exit=$?"
