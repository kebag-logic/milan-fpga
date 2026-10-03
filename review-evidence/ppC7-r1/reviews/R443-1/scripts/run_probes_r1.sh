#!/usr/bin/env bash
# Launch the round's RTL fault probes concurrently (each in its own copy), log + rc per probe
PK=$REVIEWS/ppC7-r443-1-packet; R=$PK/receipts; S=$PK/scratch
export PATH=$S/bin:$PATH VJ=3
N=hdl/aecp/KL_aecp_notify.sv
run() { "$PK/scripts/probe.sh" "$1" "$S/headctr" "$2" "$3" "$S/probes" > "$R/$1.log" 2>&1; echo $? > "$R/$1.rc"; }
run P1_notify_window_900 $N "s/(now_ms_i - ctr_last_r\[c\]) >= 32'd1000/(now_ms_i - ctr_last_r[c]) >= 32'd900/" &
run P2_notify_window_950 $N "s/(now_ms_i - ctr_last_r\[c\]) >= 32'd1000/(now_ms_i - ctr_last_r[c]) >= 32'd950/" &
run P3_notify_avb_any_index $N "500s/(ev_ctr_index_i == 16'd0)/1'b1/" &
wait
