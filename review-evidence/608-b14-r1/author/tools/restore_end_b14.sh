#!/usr/bin/env bash
# Lane B14 item 8: release the two soak bindings this lane made, then read back every restored item
# (one locked action). usage: restore_end_b14.sh; endpoints from B14_ENV (private).
set -u
set -a; . "${B14_ENV:?}"; set +a
T=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$T"); O=$P/restore; R=$VALIDATION_STORAGE/608-b14-raw/soak
mkdir -p "$O"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" unbind-a-aaf unbind peer 0 dut 0 > /dev/null; echo "UNBIND_A_AAF=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" unbind-a-crf unbind peer 2 dut 1 > /dev/null; echo "UNBIND_A_CRF=$?"
sleep 2
timeout 70 python3 -B "$T/bindops_b14.py" "$O" final-maps maps dut 0 peer 0 > /dev/null; echo "MAPS=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" final-peer-in8 state dut 1 peer 8 > /dev/null; echo "STATE_PEER_IN8=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" final-dut-in0 state peer 0 dut 0 > /dev/null; echo "STATE_DUT_IN0=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" final-dut-in1 state peer 2 dut 1 > /dev/null; echo "STATE_DUT_IN1=$?"
RS="sudo -n timeout 25s python3 -B /tmp/608-b14/read_state.py"
for m in snapshot timing counters; do
  timeout 35 ssh -o BatchMode=yes "$CTL_HOST" "$RS $m $CTL_IFACE $PEER_EID $PEER_MAC" > "$R/$m-final.jsonl"; echo "READ_$m=$?"
done
timeout 90 python3 -B "$T/console_read.py" "$DUT_CONSOLE" "$O/console-final.txt" milan_status milan_nvm "mem_read 0x90000110 4" "mem_read 0x90000200 52" "mem_read 0x900006cc 12" "mem_read 0x900008d4 12" "mem_read 0x900008f8 8" "mem_read 0x900008e0 8" "mem_read 0x90000738 4" > /dev/null; echo "CONSOLE=$?"
