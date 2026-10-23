#!/usr/bin/env bash
# notify_mutants.py's --notify-only controls at the processor head, one build
# at a time (the suite sweep holds the other build slot).
set -u
cd $VALIDATION_STORAGE/scratch/632-a659/r3b/pp-clone
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
O=$VALIDATION_STORAGE/scratch/632-a659/r3b/mut-head
rm -rf $O; mkdir -p $O
git rev-parse HEAD > $O/HEAD.txt
date -Is > $O/start.txt
python3 tb/pp_top/notify_mutants.py --output $O --verilator $VALIDATION_STORAGE/scratch/632-a659/r3/bin/verilator --jobs 1 --only enq_dropped_configuration enq_dropped_stream_info class_4_mapped_to_rate class_9_mapped_to_control requester_not_excluded entry_seq_not_advanced stream_info_get_body stream_info_compare_applied stream_info_unset_arm_dropped configuration_compare_whole_lane configuration_unchanged_notifies configuration_running_route_dropped configuration_success_reserved_dirty configuration_refusal_notifies counter_limit_500ms fan_out_skips_row_0 refresh_resets_seq foreign_unlock_allowed lock_taker_notified deregister_keeps_row registry_holds_15 set_control_ignores_lock > $O/summary.txt 2>&1
echo $? > $O/rc
date -Is > $O/end.txt
echo DONE > $O/DONE
