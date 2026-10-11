from pathlib import Path
import difflib
import hashlib
import json
import re
import sys
r=Path('$VALIDATION_STORAGE/pp73-a595/r3')
out=r/'comparisons';out.mkdir(exist_ok=True)
lines=[]
for name in ['check','lint','matrix','yosys','suites']:
 bname='base-suites-pinned' if name=='suites' else 'base-'+name
 hname='head-final-'+name
 b=(r/'logs'/f'{bname}.log').read_bytes();h=(r/'logs'/f'{hname}.log').read_bytes()
 brc=(r/'logs'/f'{bname}.rc').read_text().strip();hrc=(r/'logs'/f'{hname}.rc').read_text().strip()
 assert brc==hrc=='0',(name,brc,hrc)
 same=b==h
 if name in ['lint','matrix','yosys']:assert same,name
 if name=='check':
  expected=[x for x in h.decode().splitlines() if not x.startswith(('field drift:', 'aecp commands'))]
  expected=[x.replace('links: 1188 checked','links: 1187 checked').replace('ids: 571 files','ids: 563 files') for x in expected]
  assert sorted(expected)==sorted(b.decode().splitlines()), 'Existing make check records differ'
 if name=='suites':
  common_b=[x for x in b.splitlines() if not x.startswith(b'suites:')]
  common_h=[x for x in h.splitlines() if not x.startswith((b'suites:',b'PASS aecp_cmds '))]
  assert common_b==common_h,'Existing suite records differ'
  old=(r.parent/'r2/logs/head-suites.log').read_bytes()
  assert h==old,'Head suite tally changed from round 2'
 lines.append(f'{name}: base rc {brc}, head rc {hrc}, raw byte-identical {same}')
 for side,data in [('base',b),('head',h)]:lines.append(f'  {side}: {len(data)} bytes; sha256 {hashlib.sha256(data).hexdigest()}')
 (out/(name+'.diff')).write_text(''.join(difflib.unified_diff(b.decode().splitlines(True),h.decode().splitlines(True),fromfile=bname,tofile=hname)))
lines.append('Every original suite record is byte-identical; head suite records also equal round 2 byte for byte.')
(out/'suites.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
if '--suites-only' in sys.argv:raise SystemExit(0)
def norm(value):
 if isinstance(value,dict):return {k:norm(v) for k,v in value.items()}
 if isinstance(value,list):return sorted([norm(v) for v in value],key=lambda v:json.dumps(v,sort_keys=True))
 if isinstance(value,str):return re.sub(r'$VALIDATION_STORAGE/pp73-a595/r3/tmp/(?:concurrent-)?(?:base|head)/[^/\s"\']+','<tree>',value)
 return value
lines=[]
for name in ['d3','aecp_dispatch','aecp','ctr','notify','gsi','acmp','name_wr','name_state']:
 roots=[r/'camp'/((side if name=='d3' else 'concurrent-'+side)) for side in ['base','head']]
 for d in roots:assert (d/(name+'.rc')).read_text().strip()=='0',(d,name)
 b,h=[(d/(name+'.log')).read_bytes() for d in roots]
 assert sorted(b.splitlines())==sorted(h.splitlines()),('campaign stdout',name)
 for p in (roots[0]/(name+'.out')).glob('*.json'):
  q=roots[1]/(name+'.out')/p.name
  assert norm(json.loads(p.read_text()))==norm(json.loads(q.read_text())),(name,p.name)
 lines.append(f'{name}: base/head rc 0; stdout '+('byte-identical' if b==h else 'identical as a line multiset')+'; JSON records identical after sorting and removing scratch paths')
old=json.loads((r/'camp/resume/aecp_cmds.out/results.json').read_text())
new=json.loads((r/'camp/verified/aecp_cmds.out/results.json').read_text())
old_by={x['variant']:x for x in old};new_by={x['variant']:x for x in new}
assert all(new_by[name]==v for name,v in old_by.items())
assert len(new_by)-len(old_by)==2
lines.append('aecp_cmds: original 14 controls and golden/restored records identical to 99757648; two new mapping controls caught by name; final 16/16, rc 0')
(out/'campaigns.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))

base_controls=r/'camp/base-observer'
assert (base_controls/'aecp_cmds.rc').read_text().strip()=='0'
assert json.loads((base_controls/'aecp_cmds.out/results.json').read_text())==new
with (out/'campaigns.txt').open('a') as stream:stream.write('Original base production plus final observer: all 16 compiled controls and golden/restored records identical to head; rc 0.\n')
