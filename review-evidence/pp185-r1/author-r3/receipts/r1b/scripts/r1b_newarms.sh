#!/usr/bin/env bash
# round 1b: the 16 lock controls on their own, on the lane tree, unpiped
S=$VALIDATION_STORAGE/pp185-a647; L=$LANES/pp185-ctl; R="$S/r1b/newarms"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$S/tmpdir"
rm -rf "$R/out"
"$S/scripts/gate.sh" "$R" notify_lock "$L/tb/pp_top" python3 notify_mutants.py --jobs 4 \
  --output "$R/out" --only lock_unlock_notifies_flags_zero lock_auto_unlock_flags_zero \
  lock_notification_flags_zero lock_flags_unlock_bit_only lock_timeout_keeps_flags \
  lock_timeout_flags_zero lock_flags_from_exclusion lock_job_arguments_dropped \
  lock_job_r14_unpacked lock_notification_not_sent lock_response_flags_zero \
  lock_coalesced_timeout_keeps_flags lock_coalesced_timeout_flags_zero \
  lock_take_keeps_old_flags lock_release_keeps_old_flags register_refused
