#!/bin/sh
# Phase 2: the author's planted arms that answer the prior findings, rerun at the exact head
# from a git-archive copy (each driver plants in private temporary copies of its own).
# Run one campaign at a time, with few jobs, to stay inside a 10 GB memory cap.
# usage: run_phase2.sh <packet dir> <verilator>
set -u
P=$1
V=$2
T=$P/scratch/trees/head
R=$P/receipts
S=$P/scratch/campaigns
mkdir -p "$R" "$S"
acmp() { # receipt-name jobs arms...
  name=$1; jobs=$2; shift 2
  rm -rf "$S/$name"
  ( cd "$T" && python3 tb/pp_top/acmp_mutants.py --output "$S/$name" --verilator "$V" --jobs "$jobs" --only "$@" \
      > "$R/acmp_mutants-$name.log" 2>&1; echo $? > "$R/acmp_mutants-$name.rc" )
}
acmp round4-talker 4 move_ignores_left_ids record_lapses_in_one_epoch record_overwritten_while_young \
     cursor_reenters_early cursor_guard_three_epochs blocked_move_declares_at_once \
     disable_keeps_declared_id publish_upper_from_slot0 pcp_skips_the_gap
acmp moved_open_skips_leave 2 moved_open_skips_leave
acmp round1-talker 4 pcp_after_withdrawal_skips_the_gap pcp_pending_not_held move_lost_on_disable
acmp round1-pp_top 2 conflict_keeps_old_wait conflict_reuses_old_id reopen_sends_new
rm -rf "$S/srp"
( cd "$T" && VERILATOR="$V" python3 tb/srp_top/mutants.py --output "$S/srp" --jobs 4 \
    --only talker-reopen-abandons-leave,talker-park-never-retires,talker-reopen-parks-own-stream,talker-rebind-back-keeps-park,talker-lo-not-owed,talker-unrecorded-applicant-owes,talker-close-keeps-join,talker-park-retires-on-txla,talker-parked-applies-rx,talker-park-keeps-matcher,walk-ignores-talker-leave-copy,lwid-read-source-0,lwtsp-read-at-gate-source,lwid-written-from-source-0,talker-leave-copy-rewritten-while-parked \
    > "$R/srp_mutants-leave-copy.log" 2>&1; echo $? > "$R/srp_mutants-leave-copy.rc" )
