#!/usr/bin/env bash
# B16c dry run (offline, no bench access): run_b16c.py against the stand-ins in this directory.
# usage: dryrun_b16c.sh <work_dir> <scenario> <out.json>
#   scenarios: bcrf, baaf (nominal); refuse (the DUT's set refused); term (SIGTERM 20 s into a 30 s window);
#   music (the owner's music found at the third check, before the binds); nolock (the servo never LOCKED);
#   peer0 (the peer found on CLOCK_SOURCE 0, not as recorded); agentdies (the controller agent ends at the AAF bind)
set -u
H=$(cd "$(dirname "$0")" && pwd); W=$1; S=$2; OUT=$3
T=$W/$S; rm -rf "$T"; mkdir -p "$T/pk/tools" "$T/raw" "$T/fake"
cp "$H/../run_b16c.py" "$H/../console_poll_b8.py" "$H/../console_read.py" "$H/../b6_tone.py" "$T/pk/tools/"
export FAKE_DIR=$T/fake FAKE_TOOLS=$H PATH=$H/bin:$PATH
export CTL_HOST=ctl CTL_IFACE=if0 CTL_STAGE=/tmp/x PEER_EID=1111111111110000 PEER_MAC=111111111111 SOC_SSH=soc \
  TAP_HOST=tap TAP_PEER_IF=p TAP_DUT_IF=d CAP_CARD=fake CAP_NCH=2 CAP_FMT=fake TONE_PROC=$T/fake/tone-status
MODE=bcrf; SECS=12
case $S in baaf) MODE=baaf;; refuse) export FAKE_REFUSE_DUT_SET=1;; term) SECS=30;; music) export FAKE_MUSIC_AT=3;;
  nolock) export FAKE_NO_LOCK=1;; agentdies) export FAKE_DIE_AT_BIND=1;; peer0) export FAKE_PEER_CLK0=0;; esac
python3 -B "$H/fake_console.py" "$T/fake" > "$T/fake/console-path" & CPID=$!
( n=0; while :; do printf 'state: RUNNING\ntrigger_time: 1.5\nhw_ptr: %d\n' $n > "$T/fake/tone-status.tmp"; mv "$T/fake/tone-status.tmp" "$T/fake/tone-status"; n=$((n+4800)); sleep 0.1; done ) & TPID=$!
sleep 1; export DUT_CONSOLE=$(head -1 "$T/fake/console-path")
python3 -B "$T/pk/tools/run_b16c.py" "dry-$S" "$T/raw" "$MODE" "$SECS" > "$T/stdout.txt" 2> "$T/stderr.txt" & RPID=$!
if [ "$S" = term ]; then sleep 75; kill -TERM $RPID; fi
wait $RPID; RC=$?
kill $CPID $TPID 2>/dev/null; wait 2>/dev/null
python3 -I "$H/check_dryrun_b16c.py" "$T" "$S" "$RC" "$OUT"
