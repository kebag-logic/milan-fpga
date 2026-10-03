#!/usr/bin/env bash
# Lane B8, assignment item 4: the ONE authorised cold power cycle of the DUT, under the bench lock.
# The power strip's documented command for the DUT's outlet 0 only ("off 0; sleep 8; on 0"), run on
# the strip's host (STRIP_HOST, private). Before it: the strip's status; if the status fails, the
# host's interface list is recorded instead and NOTHING is switched (the assignment's STOP rule).
# Across it: console_listen.py records the DUT's console for 90 s without typing. After it: the
# strip's status, then the UART grader (scripts/baremetal_uart_smoke.py) every 15 s until it
# passes or 300 s have passed: a pass is the boot verdict, no pass is a failed boot (STOP).
# The strip's own output stays private (/tmp/b8-a521/private); this script prints only return codes.
# usage: pc_cycle_b8.sh <packet_dir> <lane_worktree> <name>
set -u
. "${B8_ENV:?}"
P=$1; L=$2; N=$3
R=/tmp/b8-a521/raw/$N
mkdir -p "$R" "$P/runs/$N"
timeout -k 5 570 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; L=$1; N=$2; R=$3
V=/tmp/b8-a521/private
SSH="ssh -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 $STRIP_HOST"
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 30 $SSH "powerstrip status" > "$V/strip-before.txt" 2>&1
S=$?
echo "STATUS_BEFORE_RC=$S"
if [ $S -ne 0 ]; then
  timeout 30 $SSH "ip -br addr" > "$V/strip-host-ifaces.txt" 2>&1
  echo "IFACES_RC=$? NOT_CYCLED"
  echo "UNLOCK $(date -u +%FT%T.%3NZ)"
  exit 3
fi
timeout 120 python3 -B "$P/tools/console_listen.py" "$DUT_CONSOLE" "$R/boot-console.jsonl" 90 > "$R/boot-listen.out" 2>&1 &
LP=$!
sleep 2
echo "CYCLE_BEGIN $(date -u +%FT%T.%3NZ)"
timeout 60 $SSH "powerstrip off 0; sleep 8; powerstrip on 0" > "$V/strip-cycle.txt" 2>&1
echo "CYCLE_RC=$? $(date -u +%FT%T.%3NZ)"
timeout 30 $SSH "powerstrip status" > "$V/strip-after.txt" 2>&1
echo "STATUS_AFTER_RC=$?"
wait $LP
echo "LISTEN_RC=$? $(date -u +%FT%T.%3NZ) $(cat "$R/boot-listen.out")"
T0=$(date +%s)
K=0
while :; do
  timeout 60 python3 -B "$L/scripts/baremetal_uart_smoke.py" --port "$DUT_CONSOLE" > "$P/runs/$N/grader-boot-$K.txt" 2>&1
  G=$?
  echo "GRADER_$K RC=$G $(date -u +%FT%T.%3NZ)"
  [ $G -eq 0 ] && { echo "BOOT_PASS"; break; }
  if [ $(( $(date +%s) - T0 )) -ge 300 ]; then echo "BOOT_FAIL"; break; fi
  K=$((K+1))
  sleep 15
done
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$L" "$N" "$R"
echo "LOCK_RC=$?"
