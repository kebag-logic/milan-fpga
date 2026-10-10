#!/usr/bin/env bash
# Lane B14 items 5-7: soak setup under the bench lock (one locked action).
# Reads the as-found inventory, timing and counters (B13's read_state.py), the DUT's audio maps and the
# console words, binds B13's two peer-to-DUT soak bindings with the binding rule (the two DUT-to-peer
# ones are in place as found), then writes the soak state (t0 = 30 s after the binds).
# usage: soak_setup_b14.sh; endpoints from B14_ENV (private).
set -u
set -a; . "${B14_ENV:?}"; set +a
T=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$T"); O=$P/soak; R=$VALIDATION_STORAGE/608-b14-raw/soak
mkdir -p "$O" "$R"
[ -e "$R/state.json" ] && { echo "state exists"; exit 2; }
RS="sudo -n timeout 25s python3 -B /tmp/608-b14/read_state.py"
for m in snapshot timing counters; do
  timeout 35 ssh -o BatchMode=yes "$CTL_HOST" "$RS $m $CTL_IFACE $PEER_EID $PEER_MAC" > "$R/$m-prebind.jsonl"; echo "READ_$m=$?"
done
timeout 60 python3 -B "$T/console_read.py" "$DUT_CONSOLE" "$O/console-prebind.txt" milan_status "mem_read 0x90000110 4" "mem_read 0x90000200 52" "mem_read 0x900006cc 12" "mem_read 0x900008d4 12" "mem_read 0x900008f8 4" > /dev/null; echo "CONSOLE=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" maps-prebind maps dut 0 peer 0 > /dev/null; echo "MAPS=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" bind-a-aaf bind peer 0 dut 0 > /dev/null; echo "BIND_A_AAF=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" bind-a-crf bind peer 2 dut 1 > /dev/null; echo "BIND_A_CRF=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" state-b-aaf state dut 0 peer 0 > /dev/null; echo "STATE_B_AAF=$?"
timeout 70 python3 -B "$T/bindops_b14.py" "$O" state-b-crf state dut 1 peer 8 > /dev/null; echo "STATE_B_CRF=$?"
sleep 10
timeout 35 ssh -o BatchMode=yes "$CTL_HOST" "$RS timing $CTL_IFACE $PEER_EID $PEER_MAC" > "$R/timing-postbind.jsonl"; echo "READ_timing_post=$?"
timeout 35 ssh -o BatchMode=yes "$CTL_HOST" "$RS counters $CTL_IFACE $PEER_EID $PEER_MAC" > "$R/counters-postbind.jsonl"; echo "READ_counters_post=$?"
python3 - "$R" <<'PY'
import json,sys,time
R=sys.argv[1]
timing=[json.loads(l) for l in open(f"{R}/timing-postbind.jsonl")]
cnt=[json.loads(l) for l in open(f"{R}/counters-postbind.jsonl")]
prev={f"{r['role']}|{r['descriptor_type']}|{r['descriptor_index']}":r for r in cnt}
st=dict(t0=time.time()+30,poll=0,chunks=0,timing0=timing,previous=prev)
open(f"{R}/state.json","w").write(json.dumps(st)+"\n")
print("T0", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st["t0"])))
PY
