#!/usr/bin/env bash
# The two controls of the reviewer probes: the same probe tree with the
# round-2 listener RTL, and with the round-3 arm settled-link-flush-dropped.
# usage: probe_controls.sh <clean-head-tree> <scratch-dir> <receipts-dir> <probes.inc>
set -u
src=$1; S=$2; R=$3; inc=$4; here=$(cd "$(dirname "$0")" && pwd)
bash "$here/make_probe_tree.sh" "$src" "$S/probe-r2rtl" "$inc"
git -C "$src" show a2fce4326ebdaf398a1920d79a664d44e6f1e5dd:hdl/srp/KL_srp_listener_fsm.sv \
  > "$S/probe-r2rtl/hdl/srp/KL_srp_listener_fsm.sv"
bash "$here/make_probe_tree.sh" "$src" "$S/probe-mut" "$inc"
( cd "$S/probe-mut" && git init -q . && git apply "$src/tb/srp_top/mutations/settled-link-flush-dropped.patch" )
( cd "$S/probe-r2rtl/tb/srp_stream_fsms" && make -j8 RUN_ARGS=suite > "$R/probe-on-round2-listener.log" 2>&1; echo $? > "$R/probe-on-round2-listener.rc" ) &
( cd "$S/probe-mut/tb/srp_stream_fsms" && make -j8 RUN_ARGS=suite > "$R/probe-under-settled-link-flush-dropped.log" 2>&1; echo $? > "$R/probe-under-settled-link-flush-dropped.rc" ) &
wait
