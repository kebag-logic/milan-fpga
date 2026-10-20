#!/bin/bash
# Runs milan_dp's twelve ordinary legs (built by `make run`) through sim_pool at the ceiling of 2, then render_mutants.
T=${1:?usage: milandp_pool.sh TREE   (a tree where `make -C tb/verilator/milan_dp run` built every ordinary leg)}
cd "$T/tb/verilator/milan_dp" || exit 99
# the pinned Verilator must be first on PATH (the caller exports it)
python3 sim_pool.py --jobs="2" ./obj_dir/Vmilan_dp_sim --banner "---- Milan 5.4.5 notifications and the #508 GET_STREAM_INFO seam, TIMED on the compressed processor timebase ----" ./obj_notify/Vmilan_dp_notify --banner "---- #530 CRF talker licence and per-type LeaveAll, TIMED on one compressed grid ----" ./obj_crflic/Vmilan_dp_crflic --banner "---- #658 the power-on audio maps, Milan 5.4.2.7 and a restored format ----" ./obj_dynmap/Vmilan_dp_dynmap ./obj_nxn/Vmilan_dp_nxn --banner "---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----" ./obj_nxndv/Vmilan_dp_nxndv ./obj_nxn8/Vmilan_dp_nxn8 --banner "---- the shipping Arty shape: 4 streams x 4 wire channels ----" ./obj_nxn4c/Vmilan_dp_nxn4c --banner "---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----" ./obj_nolpf/Vmilan_dp_nolpf --banner "---- all six tier-1 blocks pruned ----" ./obj_prune/Vmilan_dp_prune --banner "---- THE SHIPPING ALINX SHAPE: 1 stream x 8 wire channels, TDM8 master ----" ./obj_ax1x1/Vmilan_dp_ax1x1 --banner "---- the same shape at the TRUE clk_audio ratio (391/1591) ----" ./obj_aclk/Vmilan_dp_aclk
r1=$?
python3 render_mutants.py
r2=$?
echo "sim_pool rc=$r1 render_mutants rc=$r2"
exit $(( r1 || r2 ))
