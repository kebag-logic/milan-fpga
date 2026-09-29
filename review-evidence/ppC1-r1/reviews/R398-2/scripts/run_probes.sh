#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R398-2: reproduce this packet's executed evidence at processor head 412efeb7.
# Usage: run_probes.sh <processor clone at 412efeb7> <work dir> <verilator 5.050>
# Every write goes under <work dir>; the clone is only read (git archive).
set -eu
SRC=$1; WORK=$2; V=$3
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$WORK/logs" "$WORK/tmp"
"$V" --version | tee "$WORK/logs/verilator_version.txt"
rm -rf "$WORK/head" && mkdir -p "$WORK/head"
git -C "$SRC" archive 412efeb750e358a65b04bae1cbb3086134d15b7e | tar -x -C "$WORK/head"
H=$WORK/head
BIN=$(dirname "$V"); export PATH="$BIN:$PATH" TMPDIR="$WORK/tmp"

# 1. srp_top at head: the complete default run, then the groups one by one
make -C "$H/tb/srp_top" run > "$WORK/logs/head_srp_top_default.log" 2>&1
for g in armdelay restart peer; do
  "$H/tb/srp_top/obj_dir/Vsrp_top_sim" "$g" > "$WORK/logs/head_srp_top_$g.log" 2>&1
done

# 2. checked-in mutant arms that round 2 added or re-measured
cd "$H/tb/srp_top"
python3 mutants.py --output "$WORK/mutA" --only rearm-at-issue,r-rearm-no-deadline
python3 mutants.py --output "$WORK/mutB" --only r-rearm-no-inflight,r-flag-ignores-edge-peer,stale-expiry-honoured,mvrp-stale-expiry-honoured
python3 mutants.py --output "$WORK/mutC" --only draw-kind-0,expiry-only-redraw,mvrp-expiry-only-redraw
python3 mutants.py --output "$WORK/mutD" --only mvrp-passive-lost,mvrp-flag-at-expiry
python3 mutants.py --output "$WORK/mutE" --only pending-peer-ignored,leaveall-expiry-lost,preparation-before-slot
cd "$WORK"

# 3. now_ms wrap: the timebase wraps 5, 12 and 16 s after reset (plus a
#    base-0 control of the probe itself), and a non-wrap-safe guard control
G="armdelay restart peer timers"
for b in 00000000 FFFFEC78 FFFFD120 FFFFC180; do
  python3 "$HERE/probe_guard.py" wrap --src "$H" --work "$WORK/wrap-$b" --base "$b" --verilator "$V" $G \
    > "$WORK/logs/probe_wrap-$b.log" 2>&1 || true
done
for b in FFFFD120 FFFFC180; do
  python3 "$HERE/probe_guard.py" wrap --src "$H" --work "$WORK/wrap-$b-u" --base "$b" --unsigned --verilator "$V" $G \
    > "$WORK/logs/probe_wrap-$b-unsigned.log" 2>&1 || true
done

# 4. a dropped re-arm after a received LeaveAll: head guard vs the issue-time guard
python3 "$HERE/probe_guard.py" drop --src "$H" --work "$WORK/drop-head" --verilator "$V" \
  > "$WORK/logs/probe_drop_head.log" 2>&1
python3 "$HERE/probe_guard.py" drop --src "$H" --work "$WORK/drop-issueguard" --verilator "$V" \
  --patch "$H/tb/srp_top/mutations/rearm-at-issue.patch" > "$WORK/logs/probe_drop_issueguard.log" 2>&1
grep -h 'DROPPROBE' "$WORK/logs/probe_drop_"*.log
