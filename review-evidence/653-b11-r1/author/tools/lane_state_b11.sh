#!/usr/bin/env bash
# Lane B11 copy of lane B10's lane_state_b10.sh: only the environment name (B11_ENV) and the controller staging (/tmp/a535) differ; this lane runs only its read verb.
# Lane B10 (new): one locked controller action through lane B8's agent (b8_ctl.py agent), for the
# lane-level state changes this lane's as-found state needs. As found, the DUT's CLOCK_DOMAIN read
# CLOCK_SOURCE 1 and its STREAM_PORT_INPUT 0 held one mapping (stream 0 channel 0 to cluster 0),
# where lanes B7 to B9 found CLOCK_SOURCE 0 and both maps empty, and their run and probe tools
# assume that start. So:
#   prep     GET_CLOCK_SOURCE; SET_CLOCK_SOURCE 0 on the DUT's CLOCK_DOMAIN (the listener's),
#            read back; GET_AUDIO_MAP; the one as-found mapping removed, read back; formats read
#   restore  the one mapping added back, read back; SET_CLOCK_SOURCE 1, read back; formats read
#   read     the same reads, nothing set
# usage: lane_state_b10.sh <packet_dir> <prep|restore|read> <tag>
set -u
. "${B11_ENV:?}"
P=$1; OP=$2; T=$3
R='{"op":"clk","who":"dut"}
{"op":"map","act":"get","dtype":14,"didx":0}
{"op":"map","act":"get","dtype":15,"didx":0}
{"op":"fmt","who":"dut","dir":"in","idx":0}
{"op":"fmt","who":"dut","dir":"in","idx":1}
{"op":"fmt","who":"peer","dir":"in","idx":0}
{"op":"rx","who":"dut","idx":0}
{"op":"rx","who":"dut","idx":1}
{"op":"rx","who":"peer","idx":0}'
case "$OP" in
prep) Q="$R"'
{"op":"setclk","who":"dut","src":0}
{"op":"map","act":"remove","dtype":14,"didx":0,"n":1}
{"op":"map","act":"get","dtype":15,"didx":0}';;
restore) Q="$R"'
{"op":"map","act":"add","dtype":14,"didx":0,"n":1}
{"op":"setclk","who":"dut","src":1}
{"op":"map","act":"get","dtype":15,"didx":0}';;
read) Q="$R";;
*) echo "unknown op $OP"; exit 2;;
esac
Q="$Q"'
{"op":"quit"}'
timeout -k 5 90 flock -w 60 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a535" && \
timeout 30 scp -q "$0/tools/avdecc_ro.py" "$0/tools/b8_ctl.py" "$CTL_HOST:/tmp/a535/"
echo "STAGE_RC=$?"
printf "%s\n" "$2" | timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a535 && sudo -n timeout 50 python3 -B b8_ctl.py agent $CTL_IFACE $PEER_EID $PEER_MAC" > "$0/restore/lane-$1.jsonl" 2> "$0/restore/lane-$1.err"
echo "AGENT_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T" "$Q"
echo "LOCK_RC=$?"
