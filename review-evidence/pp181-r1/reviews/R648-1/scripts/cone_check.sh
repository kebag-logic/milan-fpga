#!/usr/bin/env bash
# RTL-level cone check at the two module boundaries of the cut, base and head.
#  notify: which output ports lie in the combinational fan-out of cmdq_count_r
#  router: whether evt_ack_i combinationally reaches the scan (gnt_found_w,
#          gnt_src_w) and which cells it drives at sel_r
# Traversal stops at every flop and memory cell, so only same-cycle logic is
# followed. usage: cone_check.sh <tree> <workdir> <tag>
set -u
tree=$1; wd=$2; tag=$3
SV2V=${SV2V:-$VALIDATION_TOOLS/sv2v-v0.0.12/sv2v}
YOSYS=${YOSYS:-yosys}
mkdir -p "$wd"
STOP='$dff,$dffe,$sdff,$sdffe,$sdffce,$adff,$adffe,$aldff,$aldffe,$dffsr,$dffsre,$mem_v2,$memwr_v2,$memrd_v2'
"$SV2V" "$tree/hdl/common/pp_pkg.sv" "$tree/hdl/aecp/KL_aecp_notify.sv" >"$wd/notify.v" || exit 3
"$SV2V" "$tree/hdl/packet_engine/KL_pp_event_router.sv" >"$wd/evr.v" || exit 3
cat >"$wd/notify.ys" <<EOF
read_verilog $wd/notify.v
chparam -set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1 KL_aecp_notify
hierarchy -top KL_aecp_notify
proc; flatten; opt_clean
tee -o $wd/notify_count_to_outputs.txt select -list w:cmdq_count_r %co*:-$STOP o:* %i
EOF
cat >"$wd/evr.ys" <<EOF
read_verilog $wd/evr.v
hierarchy -top KL_pp_event_router
proc; opt_clean
tee -o $wd/evr_ack_to_scan.txt select -list w:evt_ack_i %co*:-$STOP w:gnt_found_w w:gnt_src_w %u %i
tee -o $wd/evr_ack_to_sel_d.txt select -list w:evt_ack_i %co*:-$STOP w:sel_next_w w:gnt_src_w w:base_w w:pend_after_w %u %u %u %i
EOF
"$YOSYS" -q -l "$wd/notify.log" "$wd/notify.ys" >/dev/null 2>&1 || { echo "$tag notify yosys failed"; exit 4; }
"$YOSYS" -q -l "$wd/evr.log" "$wd/evr.ys" >/dev/null 2>&1 || { echo "$tag evr yosys failed"; exit 4; }
echo "== $tag: notify output ports combinationally fed by cmdq_count_r"
grep -v '^$' "$wd/notify_count_to_outputs.txt" | sed 's/^/  /' || echo "  (none)"
echo "== $tag: router scan signals combinationally fed by evt_ack_i"
grep -v '^$' "$wd/evr_ack_to_scan.txt" | sed 's/^/  /' || echo "  (none)"
echo "== $tag: router base/pending/next-select signals combinationally fed by evt_ack_i"
grep -v '^$' "$wd/evr_ack_to_sel_d.txt" | sed 's/^/  /' || echo "  (none)"
