"""Refresh the handoff from completed cycle records."""
from pathlib import Path
import json,math,statistics
p=Path(__file__).resolve().parent.parent
rows=[];summary=[]
for direction in ['listener','talker']:
 a=[json.loads(f.read_text()) for f in sorted(p.glob(direction+'-[0-9][0-9][0-9]/result.json'))]
 streak=0
 for r in a:
  streak=streak+1 if r['status']=='FAIL' else 0
  lat='>=30 (censored)' if r.get('latency_s') is None else f"{r['latency_s']:.9f}"
  rows.append(f"| {direction} | {r['name']} | {r.get('disconnect_hold_s',0):.6f} | {r.get('response_ns')} | {r.get('first_avtp_ns')} | {lat} | {streak} | {r['name']}/tap.pcap | {r['status']} |")
 v=sorted(r['latency_s'] for r in a if r.get('latency_s') is not None)
 s=[f'{min(v):.9f}',f'{statistics.median(v):.9f}',f'{v[math.ceil(.95*len(v))-1]:.9f}',f'{max(v):.9f}'] if v else ['unavailable']*4
 summary.append('| DUT '+direction+' | '+str(len(a))+' | '+' | '.join(s)+' | '+('FAIL' if any(r['status']=='FAIL' for r in a) else 'pending' if len(a)<100 else 'PASS')+' |')
text='''# [A386] Reconnect measurement handoff

Refs #75. Branch: 75-reconnect-bench.
Base: 8bc97021f28fb7f729418d3a00851c84ea0b50fd.
Identity: PASS. State: measurements in progress.

## Restore target and safety

All 18 original stream states unbound; both clocks internal.
No rate, format, clock, power, firmware or wiring change.
CRF pairs: reference output 2 to DUT input 1;
DUT output 1 to reference input 8, one direction at a time.
Full original census: census-start.jsonl.
Unbind the active pair after each direction.
Remove staged scripts and unload the temporary capture driver.
Each action releases its lock and joins every child before returning.
No detached process. Raw captures stay under /tmp/a386.

## Distribution in seconds

| Direction | Cycles | Min | Median | p95 | Max | Bound result |
|---|---|---|---|---|---|---|
'''+ '\n'.join(summary)+'''

## Cycle ledger

Times are relative tap nanoseconds; holds are seconds.

| Direction | Cycle | Disconnect hold | Response | First AVTP | Latency seconds | Consecutive overruns | Capture | Result |
|---|---|---|---|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

## Remaining work

Complete assigned direction counts or early stop; restore and verify.
Analyze growth and sender-attributed MSRP; write findings; run gates.
Commit locally and publish the authorized final issue comment.
'''
(p/'HANDOFF.md').write_text(text)
print('\n'.join(summary))
