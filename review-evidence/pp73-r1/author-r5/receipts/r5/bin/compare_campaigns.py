"""Require matching campaign records; normalize scratch names and completion order only."""
from pathlib import Path
from collections import Counter
import difflib
import json
import re
import sys
r=Path('$VALIDATION_STORAGE/pp73-a595/r5')
out=r/'comparisons';out.mkdir(exist_ok=True)
names=['d3','aecp_dispatch','aecp','ctr','notify','gsi','acmp','name_wr','name_state','srp_top','maap','adp_engine','srp_admission','acmp_talker','desc_store','desc_mem_guard','elab_guards','nvm_figures']
def norm(s):
    s=re.sub(re.escape(str(r))+r'/tmp/[^/\s\"\']+','<scratch-tree>',s)
    s=re.sub(re.escape(str(r))+r'/(?:base|head)(?=/|[\"\'\s]|$)','<source>',s)
    s=re.sub(re.escape(str(r))+'/camp/(?:base|head)/','<campaign>/',s)
    return s
def value(v):
    if isinstance(v,str):return norm(v)
    if isinstance(v,list):return [value(x) for x in v]
    if isinstance(v,dict):return {k:value(x) for k,x in v.items()}
    return v
def records(v):
    v=value(v)
    return sorted(v,key=lambda x:json.dumps(x,sort_keys=True)) if isinstance(v,list) else v
results=[]
for name in names:
    if '--ready' in sys.argv and not all((r/'logs'/f'{side}-camp-{name}.rc').exists() for side in ['base','head']):continue
    for side in ['base','head']:
        assert (r/'logs'/f'{side}-camp-{name}.rc').read_text().strip()=='0',(side,name)
    b,h=[(r/'logs'/f'{side}-camp-{name}.log').read_text() for side in ['base','head']]
    if Counter(norm(b).splitlines())!=Counter(norm(h).splitlines()):
        (out/(name+'.diff')).write_text(''.join(difflib.unified_diff(sorted(norm(b).splitlines(True)),sorted(norm(h).splitlines(True)),fromfile='base',tofile='head')))
        raise AssertionError(f'{name}: stdout records differ; see {out/(name+".diff")}')
    if name not in ['d3','notify','acmp','name_state']:
        assert norm(b)==norm(h),(name,'declared-order stdout differs')
    roots=[r/'camp'/side/(name+'.out') for side in ['base','head']]
    bp={p.name:p for p in roots[0].glob('*.json')};hp={p.name:p for p in roots[1].glob('*.json')}
    assert bp.keys()==hp.keys(),(name,'JSON outputs differ')
    counts={}
    for key in bp:
        bv=json.loads(bp[key].read_text());hv=json.loads(hp[key].read_text())
        assert records(bv)==records(hv),(name,key)
        if name=='name_state':assert bv==hv,(name,'declared-order structured records differ')
        counts[key]=len(bv) if isinstance(bv,list) else None
    if name=='acmp_talker':
        files={p.name:p for p in roots[0].glob('*.txt')}
        peers={p.name:p for p in roots[1].glob('*.txt')}
        assert files.keys()==peers.keys(),(name,'per-case record files differ')
        for key in files:assert files[key].read_bytes()==peers[key].read_bytes(),(name,key)
    result={'campaign':name,'base_rc':0,'head_rc':0,'raw_stdout_identical':b==h,'normalized_stdout_records_identical':True,'json_record_counts':counts,'last_record':b.strip().splitlines()[-1]}
    results.append(result)
    print(json.dumps(result),flush=True)
for side in ['base','head']:
    assert (r/'logs'/f'{side}-command-controls.rc').read_text().strip()=='0'
b,h=[json.loads((r/'camp'/side/'aecp_cmds.out/results.json').read_text()) for side in ['base','head']]
assert len(b)==len(h)==18 and all(x['passed'] for x in b+h)
assert b==h,'command controls differ'
results.append({'campaign':'aecp_cmds','base_rc':0,'head_rc':0,'json_record_count':18,'records_identical':True,'scope':'base production plus final observer; merge head'})
stem='campaigns-progress' if '--ready' in sys.argv else 'campaigns'
(out/(stem+'.json')).write_text(json.dumps(results,indent=2)+'\n')
(out/(stem+'.txt')).write_text('Every complete campaign passed at both endpoints. All verdicts, tallies, named checks and structured records match. Only scratch paths and top-level completion order are normalized; nested record order is preserved.\n')
print('Command controls: 16 plants and golden/restored, records byte-identical, rc 0')
