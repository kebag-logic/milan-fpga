#!/usr/bin/env bash
# Start the focused head runs concurrently, each with its own log, rc and secs
# file under RCPT. Usage: launch_head_runs.sh HEAD_TREE RCPT VERILATOR_DIR
set -u
H=$1; R=$2; VD=$3
export PATH="$VD:$PATH"
mkdir -p "$R"
run() { # name dir cmd...
  local n=$1 d=$2; shift 2
  ( s=$(date +%s); cd "$d" && "$@" >"$R/$n.log" 2>&1; echo $? >"$R/$n.rc.tmp"; echo $(( $(date +%s)-s )) >"$R/$n.secs"; mv "$R/$n.rc.tmp" "$R/$n.rc" ) &
}
run notify_suite "$H/tb/aecp_notify" make
run ucpu_suite "$H/tb/ucpu" make
run pp_top_suite "$H/tb/pp_top" make
run notify_lc_mutants "$H" python3 tb/pp_top/notify_mutants.py --output "$R/notify_lc_out" --verilator "$VD/verilator" --jobs 4 --only lock_claim_beside_expiry lock_expiry_in_presented_job lock_expiry_at_holder_read lock_expiry_pending_dropped lock_expiry_round_not_relatched lock_expiry_relatch_keeps_exclusion lock_take_round_not_relatched lock_take_relatch_keeps_exclusion lock_release_round_not_relatched lock_op_ignores_due_expiry
run dispatch_rdc_mutants "$H" python3 tb/pp_top/aecp_dispatch_mutants.py --output "$R/dispatch_rdc_out" --verilator "$VD/verilator" --jobs 3 --only rdc-ctype-any,rdc-ctype-status-kept,rdc-ctype-w82-nop,rdc-ctype-w84-nop,rdc-ctype-w86-nop,rdc-ctype-w88-nop
wait
