#!/usr/bin/env python3
"""Recompute the published campaign figures and bind area inputs to the reviewed source."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--archive',default='b6f2890678684aee8483f61e393167cae02cf2da')
a=p.parse_args()
packet=Path(__file__).resolve().parents[1]
prefix='review-evidence/645-r1/author-r2c/round2c/'
def blob(path):
    return subprocess.check_output(['git','show',a.archive+':'+prefix+path],cwd=a.repo)
files=subprocess.check_output(['git','ls-tree','-r','--name-only',a.archive,prefix+'campaigns/candidate'],cwd=a.repo).decode().splitlines()
logs=[f[len(prefix):] for f in files if re.search(r'b8_.*_p\d\d\.log$',f)]
assert len(logs)==128
hist=Counter(); windows=0; transient_windows=0; empty=[]; full=[]; phases={}; omitted=0
for f in logs:
    text=blob(f).decode()
    assert 'RESULT: PASS' in text and '[FAIL]' not in text
    assert blob(f[:-4]+'.rc').strip()==b'0'
    group=f.split('/')[2]
    phases.setdefault(group,[]).append(int(re.search(r'_p(\d\d)\.log$',f)[1]))
    rows=re.findall(r'^ERROR-DISTRIBUTION: (.+) window ([\d.]+) ([\d.]+) samples (\d+) axis_hz (\d+) histogram(.*)$',text,re.M)
    assert len(rows)==4
    assert {r[0] for r in rows}=={'INTERNAL before switch','AAF after settle','[SW] AAF to CRF:','[SW] CRF to AAF:'}
    for _,begin,end,n,hz,bins in rows:
        assert float(end)>float(begin) and int(hz)==6250000
        counts=dict(tuple(map(int,t.split(':'))) for t in bins.split())
        assert sum(counts.values())==int(n) and all(c>0 for c in counts.values())
        hist.update(counts);windows+=1
    margins=re.findall(r'^MARGINS: .* empty ([\d.]+) full ([\d.]+) ticks$',text,re.M)
    assert len(margins)==3
    empty.extend(float(x) for x,_ in margins);full.extend(float(y) for _,y in margins)
    one=re.findall(r'^  info: .*settle recentre fired \(1 pulse\(s\), render recentre executed 1\); slips before it \d+, after it 0;',text,re.M)
    assert len(one)==3,(f,one)
    transient_windows+=len(one)
    omitted+=text.count('render law not graded:')
assert len(phases)==8 and all(sorted(v)==list(range(16)) for v in phases.values())
assert sum(hist.values())==320462699 and min(hist)==-1 and max(hist)==1
assert min(empty)>=1 and min(full)>=1
area=json.loads(blob('area-ooc/comparison.json'))
capture=(a.repo/'hdl/ieee1722/aaf/KL_chan_map_capture.sv').read_bytes()
assert hashlib.sha256(capture).hexdigest()==area['source_sha256']['cmc_head.sv']
dp=(a.repo/'hdl/milan/milan_datapath.sv').read_text()
start=dp.index('  localparam int unsigned SRC_SETTLE_ERR_C')
end=dp.index('  end : g_settle_recentre',start)+len('  end : g_settle_recentre')
win=next(l for l in dp.splitlines() if 'localparam int unsigned MCSRV_WIN_LOG2_C' in l)
assert hashlib.sha256((win+'\n'+dp[start:end]+'\n').encode()).hexdigest()==area['source_sha256']['piece_new.svh']
delta={k:sum(area['rows'][m+'_head'][k]-area['rows'][m+'_base'][k] for m in ('settle','cmc')) for k in ('Slice LUTs','Slice Registers')}
assert delta=={'Slice LUTs':119,'Slice Registers':82}
pullfiles=subprocess.check_output(['git','ls-tree','-r','--name-only',a.archive,prefix+'final-pullin'],cwd=a.repo).decode().splitlines()
slipped=[];recover=[]
for f in pullfiles:
    if not re.search(r'pullin_h\d+_p\d\d\.log$',f):continue
    t=blob(f[len(prefix):]).decode()
    assert 'RESULT: PASS' in t and '[FAIL]' not in t
    m=re.search(r'loopback slips (\d+) before the settle and (\d+) after:',t)
    assert m and m[2]=='0'
    if int(m[1]):slipped.append(Path(f).name)
    recover.extend(float(x) for x in re.findall(r'RECOVERY:.* duration ([\d.]+) s quiet_ticks 2048',t))
assert slipped==[f'pullin_h56_p{i:02d}.log' for i in range(4)],slipped
assert max(recover)==0.551148640
result={'archive':a.archive,'candidate_phases':128,'quiet_windows':windows,'quiet_samples':sum(hist.values()),'histogram':dict(sorted(hist.items())), 'single_action_zero_postslip_windows':transient_windows, 'minimum_empty_ticks':min(empty),'minimum_full_ticks':min(full),'late_arrival_render_law_omissions':omitted,'ooc_delta':delta,'ooc_source_hashes_match':True,'isolated_56us_slip_phases':slipped,'worst_isolated_recovery_s':max(recover),'result':'PASS'}
(packet/'receipts/public-independent-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
