#!/bin/sh
# Was the 1024 ppm guard's 4-discard resync killed by the BASE unit harness?
# Runs base sim_main.cpp against base RTL, unmutated and with the resync removed.
set -u
. "$(dirname "$0")/env.sh"
for v in clean noresync; do
  W="$PKT/scratch/base_resync/$v"
  rm -rf "$W"; mkdir -p "$W"
  git -C "$CLONE" archive "$BASE_SHA" hdl tb/common tb/verilator/mmcm_servo | tar -x -C "$W"
  F="$W/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
  if [ $v = noresync ]; then
    python3 - "$F" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="if (disc_run_r == 2'(DISC_MAX_C - 1)) begin\n                win_valid_r <= 1'b0;"
assert s.count(old)==1, s.count(old)
open(p,'w').write(s.replace(old,"if (disc_run_r == 2'(DISC_MAX_C - 1)) begin\n                win_valid_r <= win_valid_r;"))
print("APPLIED base noresync")
PY
  fi
  cd "$W/tb/verilator/mmcm_servo"
  VF=$(printf '%s' "$VFLAGS_R" | sed 's/-j 8/-j 2/')
  eval "$VERILATOR $VF --top-module KL_mmcm_drp_servo -GTICK_CYC_P=3072 -GWIN_LOG2_P=5 \"-GNOM_WIN_NS_P=64'd4000000\" -GNORM_SHIFT_P=7 -GGAIN_NUM_P=7 -GRELOCK_TOUT_P=20000 -GLOCK_THR_P=8192 ../../../hdl/common/cdc_pulse.sv ../../../hdl/common/cdc_handshake.sv ../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv sim_main.cpp -o Vservo_sim" > build.log 2>&1 || echo BUILD FAILED
  echo "=== base unit ($v)"; ./obj_dir/Vservo_sim | grep -E "U10|FAIL|checks"; echo "base unit ($v) exit=$?"
done
