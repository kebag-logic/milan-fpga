#!/usr/bin/env bash
# The bench-locked part of one switch cycle (issue 117, A202, step 3).
# Run by run_cycle.sh under `flock /tmp/milan-bench.lock`; the lock is held
# for exactly this script: the console poll and the power-strip sequence.
# usage: cycle_locked.sh <out_dir> <duration_s> <pre_s> <hold_s> <outlet> <proof 0|1> <bound 0|1>
set -u
OUT=$1; D=$2; PRE=$3; HOLD=$4; O=$5; PROOF=$6; BOUND=$7
PK=$REVIEWS/117-a202-packet
P=/dev/<adapter>
SSH="ssh -o BatchMode=yes -o StrictHostKeyChecking=no"
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK $(ts)"
CMDS=(milan_status 'mem_read 0x90000780 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4')
if [ "$BOUND" = 1 ]; then CMDS+=('mem_read 0x90000750 4' 'mem_read 0x90000764 4'); fi
timeout $((D + 20)) python3 $PK/tools/console_poll.py $P $OUT/console.txt $D 0.1 "${CMDS[@]}" > $OUT/console_poll.stdout 2>&1 &
CP=$!
sleep "$PRE"
# pre-flight: no outlet is switched unless the console poll is producing samples
if ! python3 $PK/tools/console_alive.py $OUT/console.txt 2.0; then
  echo "PREFLIGHT_ABORT $(ts): console poll not producing samples; no power action"
  kill $CP 2>/dev/null; wait $CP; echo "POLL_RC=$?"; echo "UNLOCK $(ts)"; exit 5
fi
echo "PS_SEQ_START $(ts)"
timeout $((HOLD + 90)) $SSH <bench-host-prefix>pi "nohup sh /tmp/a202-ps.sh $O $HOLD > /tmp/a202-ps.log 2>&1 < /dev/null; cat /tmp/a202-ps.log; rm -f /tmp/a202-ps.log" > $OUT/powerstrip.txt 2>&1 &
PS=$!
if [ "$PROOF" = 1 ]; then
  sleep 6
  if python3 $PK/tools/console_alive.py $OUT/console.txt 2.0; then
    echo "PROOF_DUT_ALIVE $(ts)"
  else
    echo "PROOF_ABORT $(ts): DUT console silent after outlet $O off; turning it back on now"
    timeout 30 $SSH <bench-host-prefix>pi "date +%s.%N; powerstrip on $O; echo ON_RC=\$?; date +%s.%N; powerstrip status"
  fi
fi
wait $PS; echo "PS_RC=$? PS_SEQ_END $(ts)"
wait $CP; echo "POLL_RC=$?"
echo "UNLOCK $(ts)"
