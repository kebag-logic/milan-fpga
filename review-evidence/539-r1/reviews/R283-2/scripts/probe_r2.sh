#!/bin/sh
# Round-2 copy of probe.sh (only change: calls mutate_r2.py). Disposable mutation / baseline probe for tb/verilator/mmcm_servo.
# usage: probe.sh <src-tree> <work-dir> <mutant-id|none> <harness: unit|phc|rails|trace:<ns>>
# Copies the servo RTL and the mmcm_servo bench from <src-tree> into <work-dir>,
# applies one exact-string mutation (mutate.py), builds with the pinned
# Verilator at -j 1 and runs the one harness. Exit status = the harness's.
set -eu
SRC=$1; WD=$2; MUT=$3; H=$4
VERILATOR=${VERILATOR:?set VERILATOR to the pinned wrapper}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$WD"; mkdir -p "$WD/hdl/common" "$WD/hdl/ieee1722/crf" "$WD/hdl/ieee1722/aaf" "$WD/tb/common" "$WD/tb/verilator"
cp "$SRC"/hdl/common/cdc_pulse.sv "$SRC"/hdl/common/cdc_handshake.sv "$SRC"/hdl/common/cdc_pair_fifo.sv "$WD/hdl/common/"
cp "$SRC"/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv "$WD/hdl/ieee1722/crf/"
cp "$SRC"/hdl/ieee1722/aaf/KL_i2s_playback.sv "$WD/hdl/ieee1722/aaf/"
cp -r "$SRC"/tb/common/. "$WD/tb/common/"
cp -r "$SRC"/tb/verilator/mmcm_servo "$WD/tb/verilator/"
if [ "$MUT" != none ]; then python3 "$HERE/mutate_r2.py" "$WD" "$MUT"; fi
cd "$WD/tb/verilator/mmcm_servo"
VF='--cc --exe --build -j 1 -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
UG='-GTICK_CYC_P=3072 -GWIN_LOG2_P=5 "-GNOM_WIN_NS_P=64'"'"'d4000000" -GNORM_SHIFT_P=7 -GGAIN_NUM_P=7 -GRELOCK_TOUT_P=20000 -GLOCK_THR_P=8192'
C='../../../hdl/common/cdc_pulse.sv ../../../hdl/common/cdc_handshake.sv ../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv'
case "$H" in
  unit)
    eval "$VERILATOR $VF --top-module KL_mmcm_drp_servo $UG $C sim_main.cpp -o Vservo_sim" >build.log 2>&1
    exec ./obj_dir/Vservo_sim ;;
  rails)
    eval "$VERILATOR $VF --top-module rails_wrap -Mdir obj_rails $C ../../../hdl/common/cdc_pair_fifo.sv ../../../hdl/ieee1722/aaf/KL_i2s_playback.sv rails_wrap.sv sim_rails.cpp -o Vrails_sim" >build.log 2>&1
    exec ./obj_rails/Vrails_sim ;;
  phc|trace:*)
    eval "$VERILATOR $VF --public-flat-rw --top-module KL_mmcm_drp_servo -Mdir obj_phc $C sim_phc_step.cpp -o Vphc_step" >build.log 2>&1
    if [ "$H" = phc ]; then exec ./obj_phc/Vphc_step; fi
    exec ./obj_phc/Vphc_step "+trace_step_ns=${H#trace:}" ;;
  slew:*)
    eval "$VERILATOR $VF --public-flat-rw --top-module KL_mmcm_drp_servo -Mdir obj_phc $C sim_phc_step.cpp -o Vphc_step" >build.log 2>&1
    exec ./obj_phc/Vphc_step "+trace_slew_ns=${H#slew:}" ;;
esac
echo "unknown harness $H" >&2; exit 2
