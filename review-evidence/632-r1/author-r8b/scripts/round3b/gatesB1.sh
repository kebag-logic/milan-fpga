#!/usr/bin/env bash
# Processor mutation campaigns at the head, slot 2, one build at a time:
# every --notify-only control, the twelve D3 controls graded by section S,
# then tb/aecp_cmds' standing controls (a CI gate).
set -u
cd $VALIDATION_STORAGE/scratch/632-a659/r3b/pp-final-m
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
V=$VALIDATION_STORAGE/scratch/632-a659/r3/bin/verilator
O=$VALIDATION_STORAGE/scratch/632-a659/r3b/final-B
rm -rf $O; mkdir -p $O
git rev-parse HEAD > $O/HEAD.txt
date -Is > $O/start.txt
python3 tb/pp_top/notify_mutants.py --output $O/notify --verilator $V --jobs 1 --only enq_dropped_configuration enq_dropped_stream_info class_4_mapped_to_rate class_9_mapped_to_control requester_not_excluded entry_seq_not_advanced stream_info_get_body stream_info_compare_applied stream_info_unset_arm_dropped configuration_compare_whole_lane configuration_unchanged_notifies configuration_running_route_dropped configuration_success_reserved_dirty configuration_refusal_notifies counter_limit_500ms fan_out_skips_row_0 refresh_resets_seq foreign_unlock_allowed lock_taker_notified deregister_keeps_row registry_holds_15 set_control_ignores_lock > $O/notify.summary 2>&1; echo $? > $O/notify.rc
python3 tb/pp_top/d3_mutants.py --output $O/d3 --verilator $V --jobs 1 --only latch_ignores_program taint_ignored clear_wins_same_edge clear_by_group clear_by_index identify_is_a_change unchanged_compare_ignores_validity no_backoff_d3 fourth_attempt alarm_forgiven_by_success backoff_derivation backoff_holds_dispatch > $O/d3.summary 2>&1; echo $? > $O/d3.rc
python3 -B tb/aecp_cmds/mutants.py --output $O/aecp_cmds --verilator $V --jobs 1 > $O/aecp_cmds.summary 2>&1; echo $? > $O/aecp_cmds.rc
date -Is > $O/end.txt
echo DONE > $O/DONE
