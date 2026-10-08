#!/usr/bin/env bash
# Launch the reviewer's focused gates detached, each with its own log and rc file.
# usage: launch_gates.sh PACKET_DIR
set -u
P=$1; S=$P/scratch; R=$P/receipts; V=$VALIDATION_TOOLS/pinned-verilator-5.050
mkdir -p "$R/gates"
run() { # name dir cmd...
  local name=$1 dir=$2; shift 2
  ( cd "$dir" && PATH=$V:$PATH "$@" ) >"$R/gates/$name.log" 2>&1; echo $? >"$R/gates/$name.rc"
}
HEAD_ARMS="ident_burst_deadline_one_tick_short ident_t0_same_ms ix_old_identity_kept ix_new_identity_unset ix_last_chunk_ignored ix_rewrite_unmatched override_set_only own_compare_new_row stamp_read_without_valid counter_spacing_from_selection_tw counter_stamp_at_send_only counter_stamp_first_job_only dereg_mid_round_no_hold dereg_pending_stops_follow dereg_lost_at_round_end cancel_one_clock_late port_not_compared port_not_latched port_not_stored avb_counter_row_dropped avb_counter_row_collapsed avb_counter_named_clock avb_counter_any_index avb_counter_name_overlaps_clock cancel_one_per_command report_fail_ignores_probe report_rsp_ignores_probe owner_turns_dropped settle_dropped depth_shared depth_not_keyed registry_tag_port_bits monitor_tag_port_bits expiry_port_dropped"
NEW_ARMS="cancel_collision_drops_command cancel_pending_accepts_failure"
nohup bash -c "$(declare -f run); P=$P S=$S R=$R V=$V; run notify-suite-head $S/trees/head/tb/aecp_notify make -j4" >/dev/null 2>&1 &
nohup bash -c "$(declare -f run); P=$P S=$S R=$R V=$V; run notify-suite-base $S/trees/base/tb/aecp_notify make -j4" >/dev/null 2>&1 &
nohup bash -c "$(declare -f run); P=$P S=$S R=$R V=$V; run lint-head $S/trees/head ./scripts/lint_hdl.sh" >/dev/null 2>&1 &
nohup bash -c "$(declare -f run); P=$P S=$S R=$R V=$V; run make-check-head $S/headgit make check" >/dev/null 2>&1 &
nohup bash -c "$(declare -f run); P=$P S=$S R=$R V=$V; run matrix-head $S/headgit python3 scripts/gen_matrix.py --check" >/dev/null 2>&1 &
nohup bash -c "$(declare -f run); P=$P S=$S R=$R V=$V; run campaign-head $S/trees/head python3 tb/pp_top/notify_mutants.py --output $S/camp-head --verilator $V/verilator --jobs 7 --only $HEAD_ARMS $NEW_ARMS" >/dev/null 2>&1 &
nohup bash -c "$(declare -f run); P=$P S=$S R=$R V=$V; run campaign-base $S/trees/base python3 tb/pp_top/notify_mutants.py --output $S/camp-base --verilator $V/verilator --jobs 5 --only $HEAD_ARMS" >/dev/null 2>&1 &
echo launched
