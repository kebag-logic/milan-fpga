#!/bin/bash
# base_rtl.sh <clone> <out>: the head's harnesses built against the BASE RTL
# (dev a032c6d6's KL_avtp_rx_monitor_ctx.sv and KL_crf_rx.sv, byte copies via
# git show), through the suites' own recipes: the defect #775 reports, seen by
# the new [SQ] checks. Each run must FAIL; its [FAIL] lines are the evidence.
. <scratch>/scripts/env.sh
cd "$1" || exit 2
out=$2; mkdir -p "$out"; w=$TMPDIR/base-rtl; rm -rf "$w"; mkdir -p "$w"
base=a032c6d6e3775f145349d5a495c1e1ad12294936
git show $base:hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv > "$w/KL_avtp_rx_monitor_ctx.sv"
git show $base:hdl/ieee1722/crf/KL_crf_rx.sv > "$w/KL_crf_rx.sv"
sha256sum "$w"/*.sv | sed "s#$w/##" > "$out/base-rtl.sha256"
make -s -C tb/verilator/avtp_rxmon nx-build RXMON_SRC="$w/KL_avtp_rx_monitor_ctx.sv" NX_MDIR="$w/obj_nx" > "$out/nx-build.log" 2>&1
echo "nx-build rc=$?" > "$out/rc.txt"
(cd tb/verilator/avtp_rxmon && "$w/obj_nx/Vavtp_rxmon_nx_sim") > "$out/nx-base.log" 2>&1
echo "nx-run rc=$?" >> "$out/rc.txt"
make -s -C tb/verilator/crf_rx unit-build RX_RTL="$w/KL_crf_rx.sv" UNIT_MDIR="$w/obj_unit" > "$out/crf-build.log" 2>&1
echo "crf-build rc=$?" >> "$out/rc.txt"
(cd tb/verilator/crf_rx && "$w/obj_unit/Vcrf_rx_sim") > "$out/crf-base.log" 2>&1
echo "crf-run rc=$?" >> "$out/rc.txt"
make -s -C tb/verilator/crf_rx discontinuity-build RX_RTL="$w/KL_crf_rx.sv" DISC_MDIR="$w/obj_disc" > "$out/disc-build.log" 2>&1
echo "disc-build rc=$?" >> "$out/rc.txt"
(cd tb/verilator/crf_rx && "$w/obj_disc/Vdiscontinuity") > "$out/disc-base.log" 2>&1
echo "disc-run rc=$?" >> "$out/rc.txt"
grep -h "\[FAIL\]\|FAIL:" "$out/nx-base.log" > "$out/nx-base.FAIL.txt"
grep -h "\[FAIL\]" "$out/crf-base.log" > "$out/crf-base.FAIL.txt"
grep -h "FAIL" "$out/disc-base.log" > "$out/disc-base.FAIL.txt"
cat "$out/rc.txt"; wc -l "$out"/*.FAIL.txt
