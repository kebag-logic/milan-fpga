#!/usr/bin/env python3
"""Independent synthetic captures and disposable grader mutation; no source edits."""
import copy
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
(out / "scratch").mkdir(exist_ok=True)
source = repo / 'tb/tools/torture_campaign.py'
spec = importlib.util.spec_from_file_location('campaign_review', source)
tp = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = tp
spec.loader.exec_module(tp)
N, C = 20000, 4
arms = [dict(index=i, **fields) for i, fields in (
    (100, {'class':'dropped', 'n':3}), (300, {'class':'repeated', 'n':2}),
    (500, {'class':'bit-flip', 'channel':1, 'mask':0x100}),
    (19000, {'class':'dropped', 'n':3}), (19300, {'class':'repeated', 'n':2}),
    (19600, {'class':'bit-flip', 'channel':3, 'mask':0x100}))]

def capture(extra=(), omit=None):
    events = [dict(a) for a in arms if a['index'] != omit] + list(extra)
    result = bytearray()
    for i in range(N):
        shift = sum(e.get('n',0) * (1 if e['class']=='dropped' else -1)
                    for e in events if e['class'] in ('dropped','repeated') and i >= e['index'])
        values = [((c+1)*4096 + ((i+shift)%4096))*256 for c in range(C)]
        for e in events:
            if not e['index'] <= i < e['index'] + e.get('span',1):
                continue
            if e['class'] == 'bit-flip':
                values[e['channel']] ^= e['mask']
            elif e['class'] == 'silence':
                values = [0]*C
            elif e['class'] == 'swap':
                a,b=e['channels']; values[a],values[b]=values[b],values[a]
            elif e['class'] == 'copy-channel':
                values[e['destination']] = values[e['source']]
        result.extend(struct.pack('>4I',*values))
    return bytes(result)

def grade(extra=(), losses=(), omit=None):
    return tp.grade_audio_counter_capture(capture(extra,omit),
        tp.CounterCapture(C,'big',48000,100.0,200.0), tp.CounterRunLog(arms,list(losses),0))

rows=[]
for name,extra,losses,omit,expected in [
    ('clean',[],[],None,'PASS'),
    ('drop-5',[dict(index=8000,**{'class':'dropped','n':5})],[],None,'FAIL'),
    ('repeat-4',[dict(index=8000,**{'class':'repeated','n':4})],[],None,'FAIL'),
    ('silence-6',[dict(index=8000,**{'class':'silence','span':6})],[],None,'FAIL'),
    ('swap-3',[dict(index=8000,**{'class':'swap','span':3,'channels':(0,2)})],[],None,'FAIL'),
    ('missed-arm',[],[],100,'NOT RUN'),
    ('capture-loss',[dict(index=8000,**{'class':'dropped','n':9})],[{'index':8000,'frames':9}],None,'PASS'),
    ('drop-4096',[dict(index=8000,**{'class':'dropped','n':4096})],[],None,'FAIL'),
    ('drop-3000',[dict(index=8000,**{'class':'dropped','n':3000})],[],None,'FAIL'),
    ('two-low-bit-flips',[dict(index=8000,**{'class':'bit-flip','span':2,'channel':2,'mask':0x400})],[],None,'FAIL'),
    ('single-tag-bit-flip',[dict(index=8000,**{'class':'bit-flip','channel':0,'mask':0x200000})],[],None,'FAIL'),
    ('copy-channel',[dict(index=8000,**{'class':'copy-channel','span':3,'source':2,'destination':0})],[],None,'FAIL'),
]:
    verdict,detail=grade(extra,losses,omit)
    rows.append(dict(name=name,expected_verdict=expected,actual_verdict=verdict,
                     injected=extra,events=[e for e in detail.get('events',[]) if e['attribution']!='planted'],
                     missed=detail.get('planted_missed'),why=detail['why']))

items=list(tp.RELEASE_PERSISTED_ITEMS)
defaults={i:'default' for i in items}
pre={i:'nondefault' for i in items}
rows.append(dict(name='commit-target-defaults-persistence-disabled',expected_verdict='NOT RUN or FAIL',
    result=tp.check_release_state_restored(pre,defaults,defaults,items=items,phase='journal_commit',committed=defaults)))

names=['SEQ_NUM_MISMATCH','STREAM_INTERRUPTED','LATE_TIMESTAMP','EARLY_TIMESTAMP','MEDIA_UNLOCKED']
reads=[{'target':'input-0','timestamp_s':0,'values':dict.fromkeys(names,0)},
       {'target':'input-0','timestamp_s':60,'values':dict(dict.fromkeys(names,0),MEDIA_UNLOCKED=1)}]
planted=[{'target':'input-0','kind':'deliberate disturbance','window_s':[10,20]}]
rows.append(dict(name='unlock-outside-planted-window',actual_unlock_s=45,reads=reads,planted=planted,
    expected_verdict='FAIL or NOT RUN without temporal evidence',result=tp.check_release_soak_counters(
        reads,planted,targets=['input-0'],capture_complete=True)))

verdict,detail=grade([{'index':7000,'class':'dropped','n':409600},
                      {'index':8000,'class':'bit-flip','channel':0,'mask':1}],
                     [{'index':7000,'frames':409600}])
event=next(e for e in detail['events'] if e['attribution']=='dut')
rows.append(dict(name='timestamps-after-capture-loss',verdict=verdict,event=event,
                 capture_loss_frames=409600,expected_wall_s=100+(8000+409600)/48000,
                 expected_gptp_s=200+(8000+409600)/48000,
                 expected_capture_duration_s=(N+409600)/48000,
                 actual_capture_duration_s=detail['duration_s']))

# Independent assertion oracle: changing the slip count must make the shipped self-test fail.
old='words, n=abs(shift),'
new='words, n=abs(shift) + 1,'
text=source.read_text()
assert text.count(old)==1
mutant=out/'scratch'/'count_mutant.py'
mutant.write_text(text.replace(old,new))
with (out/'grader_mutant.log').open('w') as log:
    run=subprocess.run([sys.executable,'-B',str(mutant),'--self-test'],cwd=repo,stdout=log,stderr=subprocess.STDOUT,timeout=120)
(out/'grader_mutant.rc').write_text(str(run.returncode)+'\n')
assert run.returncode != 0, 'grader count mutant survived'
rows.append(dict(name='grader-count-mutant',returncode=run.returncode,result='KILLED'))
(out/'probes.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
