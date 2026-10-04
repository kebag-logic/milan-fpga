#!/usr/bin/env bash
# Lane B11 (new; lane B10's lane_state_b10.sh pattern): one locked action that returns the DUT's
# media-clock servo to its as-found IDLE state after the lane's CRF cycles left it in HOLDOVER
# with a held trim. Lane B10 found that a set to INTERNAL releases the held trim. Through lane
# B8's agent (b8_ctl.py agent) on the DUT's CLOCK_DOMAIN 0, the listener's (never the talker's):
#   GET_CLOCK_SOURCE; SET_CLOCK_SOURCE 0, read back; SET_CLOCK_SOURCE 1 (as found), read back.
# The DUT console's servo status word (0x900008F8) is read before and after (read-only).
# usage: clock_release_b11.sh <packet_dir>
set -u
. "${B11_ENV:?}"
P=$1
Q='{"op":"clk","who":"dut"}
{"op":"setclk","who":"dut","src":0}
{"op":"setclk","who":"dut","src":1}
{"op":"clk","who":"dut"}
{"op":"quit"}'
timeout -k 5 120 flock -w 60 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 30 python3 -B "$0/tools/console_read.py" "$DUT_CONSOLE" "$0/restore/servo-before-release.txt" "mem_read 0x900008f8 8" > /dev/null 2>&1
echo "DUT_BEFORE_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a535" && \
timeout 30 scp -q "$0/tools/avdecc_ro.py" "$0/tools/b8_ctl.py" "$CTL_HOST:/tmp/a535/"
echo "STAGE_RC=$?"
printf "%s\n" "$1" | timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a535 && sudo -n timeout 50 python3 -B b8_ctl.py agent $CTL_IFACE $PEER_EID $PEER_MAC" > "$0/restore/clock-release.jsonl" 2> "$0/restore/clock-release.err"
echo "AGENT_RC=$?"
sleep 2
timeout 30 python3 -B "$0/tools/console_read.py" "$DUT_CONSOLE" "$0/restore/servo-after-release.txt" "mem_read 0x900008f8 8" > /dev/null 2>&1
echo "DUT_AFTER_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$Q"
echo "LOCK_RC=$?"
