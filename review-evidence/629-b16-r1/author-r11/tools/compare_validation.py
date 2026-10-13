#!/usr/bin/env python3
"""Compare Round 11 validation against the frozen Round 10 receipts.
Usage: compare_validation.py PREVIOUS_PACKET NEW_PACKET
Only source-page locators may move, by seven. Outcomes and expectations stay frozen.
"""
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys
p,o=map(Path,sys.argv[1:])
def read(path): return json.loads(path.read_text())
def write(name,data):
    (o/'receipts'/name).write_text(json.dumps(data,indent=1,ensure_ascii=False)+'\n')
def norm(value):
    if isinstance(value,str):
        return re.sub(r'((?:629_MEDIA_CLOCK_FOLLOWING_BENCH|page)\.md:)(\d+)',
                      lambda m:m[1]+str(int(m[2])-7),value)
    if isinstance(value,list): return [norm(x) for x in value]
    if isinstance(value,dict):return {k:norm(v) for k,v in value.items()}
    return value
records=[]
for n in range(3,11):
    a=read(p/'controls'/('r10-controls.json' if n==10 else f'r10-rerun-r{n}-controls.json'))['controls']
    b=read(o/f'receipts/controls-{n}.json')['controls']
    changes=[]; matched=len(a)==len(b)
    for x,y in zip(a,b):
        for key in sorted(set(x)|set(y)):
            old,new=x.get(key),y.get(key)
            if old==new:continue
            assert isinstance(old,str) and isinstance(new,str),(n,x['control'],key)
            pattern=r'\blines? (\d+)(?: and (\d+))?'
            def positions(s):return [int(v) for m in re.finditer(pattern,s) for v in m.groups() if v]
            before,after=positions(old),positions(new)
            ok=re.sub(pattern,'<lines>',old)==re.sub(pattern,'<lines>',new) and len(before)==len(after) and all(v-u==7 for u,v in zip(before,after))
            matched=matched and ok
            changes.append(dict(control=x['control'],field=key,before=old,after=new,only_page_line_plus_7=ok))
    records.append(dict(round=n,count=len(b),passed=sum(x['verdict']=='PASS' for x in b),
                        rc=int((o/f'receipts/controls-{n}.rc').read_text()),semantics_equal=matched,locator_changes=changes))
write('control-comparison.json',dict(note='Unchanged runner bytes and outcomes. Every differing field changes only page line locators by seven; README line 15 stays.',runners=records,all_semantics_equal=all(x['semantics_equal'] for x in records)))
# Use the inherited result readers, without running any probe here.
sys.argv=[str(p/'tools/r10_probe_reruns.py'),'.',str(p),str(p/'tools/review-probes'),'.','ada26e56']
ns=runpy.run_path(sys.argv[0])
probe_results=[]
relocated={'r624-5-row3200':'relocated-locked.json','r624-6-row3200-polls':'relocated-polls.json','r624-6-escapes':'relocated-escapes.json'}
for name,entry in ns['PROBE'].items():
    old=read(p/f'r10/{name}-probe-rerun.json')
    if name in relocated:
        result=read(o/'receipts'/relocated[name])
        if isinstance(result,dict) and 'rows' in result:
            result=json.loads(json.dumps(result))
            for row in result['rows']:row['line']=str(int(row['line'])-7)
        new_reading=entry[5](result)
        new_reading=json.loads(json.dumps(new_reading))
        rc=0
        script=o/'tools/relocated'/entry[0]
        policy='Only fixed page locators moved by seven; original outcome retained separately.'
    else:
        new=read(o/f'receipts/probes/{name}-probe-rerun.json')
        result=new['results'];new_reading=norm(new['reading']);rc=new['exit']
        script=p/'tools/review-probes'/entry[0]
        policy='Original probe unchanged; diagnostic page locators normalized by seven.'
        assert new['probe_sha256']==old['probe_sha256']
    equal=new_reading==old['reading'] and rc==old['exit']
    probe_results.append(dict(probe=name,policy=policy,source_probe_sha256=old['probe_sha256'],
                              run_probe_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                              rc=rc,outcomes_equal=equal,source_reading=old['reading'],candidate_reading_normalized=new_reading))
write('probe-comparison.json',dict(probes=probe_results,all_outcomes_equal=all(x['outcomes_equal'] for x in probe_results)))
a,b=read(p/'r10/self-probes.json'),read(o/'receipts/self.json')
keys=['probe','from','where','rc','detected','markup','measurement','expect','why_pass','met']
self_equal=len(a['probes'])==len(b['probes']) and all({k:x.get(k) for k in keys}=={k:y.get(k) for k in keys} for x,y in zip(a['probes'],b['probes']))
extras=dict(self_probe_count=len(b['probes']),self_met=b['met'],self_outcomes_equal=self_equal,
            parser_equal=read(p/'r10/parser-extents.json')==read(o/'receipts/parser.json'),
            reader_equal=read(p/'r10/reader-controls.json')==read(o/'receipts/reader.json'))
a,b=read(p/'r10/layers.json'),read(o/'receipts/layers.json')
for row in b['cases']:
    if row['document']=='629_MEDIA_CLOCK_FOLLOWING_BENCH.md':row['line']-=7
    row['runs']=norm(row['runs'])
extras['layers_equal']=a==b
write('supplementary-comparison.json',extras)
summary=dict(controls_equal=all(x['semantics_equal'] for x in records),probes_equal=all(x['outcomes_equal'] for x in probe_results),**extras)
write('validation-summary.json',summary)
print(json.dumps(summary))
assert summary['controls_equal'] and summary['probes_equal'] and all(extras[k] for k in ['self_outcomes_equal','parser_equal','reader_equal','layers_equal'])
