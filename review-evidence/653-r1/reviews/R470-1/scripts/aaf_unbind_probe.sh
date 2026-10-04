#!/bin/sh
# Reviewer probe: in a DISPOSABLE copy of the tree at the head under review,
# remove the AAF bind-fall unlock (task #32) and run the timed notify leg.
# usage: aaf_unbind_probe.sh <disposable tree copy>   (needs VERILATOR set)
set -eu
T=$1
F=$T/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv
n=$(grep -c "if (bind_fall_i\[s\] && locked_sh_r\[s\]) sil_pend_r\[s\] <= 1'b1;" "$F")
[ "$n" = 1 ] || { echo "pattern count $n, expected 1"; exit 2; }
sed -i "s/if (bind_fall_i\[s\] && locked_sh_r\[s\]) sil_pend_r\[s\] <= 1'b1;/if (1'b0) sil_pend_r[s] <= 1'b1; \/\/ PROBE: AAF unbind unlock removed/" "$F"
cd "$T/tb/verilator/milan_dp" && make notify VERILATOR_JOBS=4 NOTIFY_MDIR=obj_notify_aafprobe
