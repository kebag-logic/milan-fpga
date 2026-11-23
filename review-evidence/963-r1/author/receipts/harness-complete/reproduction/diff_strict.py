#!/usr/bin/env python3
"""Strict observable differential; timing normalization is diagnostic only, never a byte-identical verdict."""
import ast, collections, hashlib, json, sys
from pathlib import Path
T=Path('<scratch>')
# Reuse only the original parser and comparison function, without its normalization/main driver.
src=ast.parse((T/'bin/diff_full.py').read_text())
ns={'collections':collections,'json':json,'Path':Path,'PUB_LO':0x200,'PUB_HI':0x280}
for node in src.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('observe','first_diff'):
  exec(compile(ast.Module(body=[node],type_ignores=[]),'diff_full.py','exec'),ns)
rows=[]; missing=[]
for tree in ('base','h4'):
 for build in sorted((T/'meas/full'/tree).glob('*/*')):
  if not build.is_dir() or not (build/'parts.json').is_file(): continue
  spec=json.loads((build/'parts.json').read_text())
  for group in sorted(g for part in spec['parts'] for g in part['groups']):
   if not (build/'g'/group/'results.json').is_file(): missing.append(f'{tree}/{build.parent.name}/{build.name}/{group}')
for run in sorted((T/'meas/full/base').glob('*/*/g/*')):
 if not (run/'results.json').is_file(): continue
 point,arm,group=run.parts[-4],run.parts[-3],run.name
 other=T/'meas/full/h4'/point/arm/'g'/group
 if not (other/'results.json').is_file(): continue
 a,b=(ns['observe'](r,group) for r in (run,other))
 d=ns['first_diff'](a,b)
 counts={}; first=None; notice_changed=0
 for channel in sorted(set(a['wire'])|set(b['wire'])):
  x,y=a['wire'].get(channel,[]),b['wire'].get(channel,[])
  changed=sum(u!=v for u,v in zip(x,y))+abs(len(x)-len(y))
  if changed: counts[str(channel)]=changed
  for k,(u,v) in enumerate(zip(x,y)):
   if u!=v:
    ub,vb=bytes.fromhex(u),bytes.fromhex(v)
    offsets=[i for i,(c,e) in enumerate(zip(ub,vb)) if c!=e]
    if first is None: first=dict(channel=channel,frame=k,offsets=offsets,base=u,head=v)
    if len(ub)>=38 and ub[14]==0xfb and int.from_bytes(ub[36:38],'big')&0x8000: notice_changed+=1
 rows.append(dict(point=point,arm=arm,group=group,exact=d is None,difference=d,changed_frames=counts,
  changed_unsolicited_frames=notice_changed,first=first,frames=sum(map(len,a['wire'].values())),
  target=group=='aecp-largest-notice',over=[a['over'],b['over']],longest=[a['longest'],b['longest']],
  stated=[a['stated'],b['stated']],rc=[a['rc'],b['rc']]))
out=T/'final4/strict'; out.mkdir(exist_ok=True)
(out/'rows.json').write_text(json.dumps(rows,indent=1)+'\n')
lines=[f'{len(rows)} paired groups; {sum(r["exact"] for r in rows)} exact; {sum(not r["exact"] for r in rows)} with raw differences; {len(missing)} missing runs.',
 'No field is masked. Frame order is retained per channel/interface. Timestamp columns alone are excluded.', '']
for r in rows:
 lines.append(f'{"EXACT" if r["exact"] else "DIFF"} {r["point"]}/{r["arm"]}/{r["group"]}: {r["frames"]} frames; share {r["over"]}; longest {r["longest"]}; {r["difference"] or "all frames, publications, probe statuses and counts identical"}')
lines+=['','Missing runs:',*missing]
(out/'diff.txt').write_text('\n'.join(lines)+'\n')
print(lines[0]); print('Target:',[(r['point'],r['arm'],r['exact']) for r in rows if r['target']])
print('Raw differences:',[(r['point'],r['arm'],r['group'],r['changed_frames']) for r in rows if not r['exact']])
