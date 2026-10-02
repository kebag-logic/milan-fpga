#!/bin/sh
# R421-4: the campaign runs behind receipts/{notify,aecp,dispatch,acmp,d3}/,
# on a scratch clone of the head (TREE) with the pinned simulator first on PATH.
# Each step fits one ten-minute foreground call; at most 8 jobs at once.
# Usage: run_campaigns.sh TREE OUT STEP
set -u
TREE=$1; OUT=$2; STEP=$3; HERE=$(cd "$(dirname "$0")" && pwd)
cd "$TREE"
case $STEP in
notify-A) python3 tb/pp_top/notify_mutants.py --output "$OUT/notify/A" --jobs 8 --only \
  inflight_highest_free_id inflight_match_ignores_seq inflight_cancel_keeps_timer inflight_shared_seq \
  ident_burst_deadline_one_tick_short ident_t0_same_ms ident_built_at_default ;;
notify-B) python3 tb/pp_top/notify_mutants.py --output "$OUT/notify/B" --jobs 8 --only \
  enq_dropped_configuration enq_dropped_stream_info class_4_mapped_to_rate class_9_mapped_to_control \
  requester_not_excluded entry_seq_not_advanced stream_info_get_body counter_limit_500ms fan_out_skips_row_0 \
  refresh_resets_seq foreign_unlock_allowed lock_taker_notified deregister_keeps_row registry_holds_15 \
  set_control_ignores_lock ;;
notify-C) python3 tb/pp_top/notify_mutants.py --output "$OUT/notify/C" --jobs 8 --only \
  ident_two_frames ident_seq_per_frame ident_no_rearm ident_rearm_from_third_frame ident_burst_100ms \
  ident_t0_at_request ident_burst_from_t0 ident_departure_is_retirement ident_departure_unwired \
  ident_next_burst_at_once ident_wait_ignores_gap ident_press_not_latched ident_burst_press_not_latched \
  ident_departure_ignores_ready ident_cut_on_release ident_release_ignored ident_unicast_da \
  ident_face_taken_mid_job ;;
aecp)  # six chunks of the 55 arms (every sixth arm), run side by side
  i=0; pids=""; tail -n 6 "$OUT/aecp/chunks.txt" > "$OUT/aecp/.c"
  while read c; do i=$((i+1)); python3 tb/pp_top/aecp_mutants.py --output "$OUT/aecp/c$i" --only "$c" \
    > "$OUT/aecp/chunk_$i.stdout" 2>&1 & pids="$pids $!"; done < "$OUT/aecp/.c"; wait $pids ;;
dispatch)  # five chunks of the 35 arms (every fifth arm), run side by side
  i=0; pids=""; while read c; do i=$((i+1)); python3 tb/pp_top/aecp_dispatch_mutants.py --output "$OUT/dispatch/c$i" \
    --only "$c" --verilator verilator > "$OUT/dispatch/chunk_$i.stdout" 2>&1 & pids="$pids $!"; done < "$OUT/dispatch/chunks.txt"; wait $pids ;;
acmp) python3 tb/pp_top/acmp_mutants.py --output "$OUT/acmp" --jobs 8 --verilator verilator ;;
d3-goldens) python3 "$HERE/d3_chunk.py" . "$OUT/d3" --goldens --jobs 3 ;;
d3-slice) python3 "$HERE/d3_chunk.py" . "$OUT/d3" --slice "$4/6" --jobs 8 ;;
esac
