#!/usr/bin/env python3
"""Check issue #117 restart clock refusal and timestamp ordering offline.

Usage: clock_controls.py PUBLIC_AUTHOR_PACKET CAPTURE_DIRECTORY OUTPUT_DIRECTORY
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import numpy as np

packet, raw, out = map(lambda p: Path(p).resolve(), sys.argv[1:4])
work = out/'scratch/clock'
work.mkdir(parents=True, exist_ok=True)
ts = np.fromfile(raw/'cap-ts.bin', dtype=[('f','<i8'),('rt','<f8'),('mono','<i8')])
events = [json.loads(s) for s in (packet/'r3/runs/rA/cycles.jsonl').read_text().splitlines() if s.startswith('{')]
pre = [e for e in events if e['kind']=='binding-rule']
binds = [e for e in events if e['kind']=='bind']
rm = ts['rt']-ts['mono']/1e9
result = dict(reads=len(ts), frames=int(ts['f'][-1]), realtime_monotonic_range_us=float(np.ptp(rm)*1e6),
              min_read_interval_ms=float(np.diff(ts['mono']).min()/1e6),
              max_read_interval_ms=float(np.diff(ts['mono']).max()/1e6),
              cumulative_frames_strictly_increasing=bool((np.diff(ts['f'])>0).all()),
              realtime_strictly_increasing=bool((np.diff(ts['rt'])>0).all()),
              cycle_precedes_bind=[a['t']<b['t'] for a,b in zip(pre,binds)],
              timestamps_cover_cycles=bool(ts['rt'][0]<pre[0]['t']<binds[-1]['t']<ts['rt'][-1]),controls=[])
for sign in [1,-1]:
    x = ts.copy()
    x['rt'][len(x)//2:] += sign*0.002
    target = work/f'step-{sign}.bin'
    x.tofile(target)
    # Refusal must precede tap access: a nonexistent tap is intentional.
    cmd = [sys.executable,'-I','-B',str(packet/'tools/pr2/b21_restart_bound.py'),str(packet/'r3/runs/rA/cycles.jsonl'),str(work/'unused.pcap'),str(raw/'cap-lr.raw'),str(target),str(work/'unused.json')]
    p = subprocess.run(cmd,capture_output=True,text=True,timeout=60,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
    text = p.stdout+p.stderr
    ok = p.returncode!=0 and 'refused: realtime moved against monotonic' in text
    result['controls'].append(dict(step_ms=sign*2,rc=p.returncode,message=text.strip(),refused=ok))
    assert ok
assert all(result['cycle_precedes_bind']) and result['timestamps_cover_cycles']
(out/'receipts/clock-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
