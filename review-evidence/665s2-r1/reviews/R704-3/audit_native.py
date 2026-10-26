#!/usr/bin/env python3
"""Decode raw observations independently and compare exact published measurements."""
import collections,hashlib,json,os,sys
from pathlib import Path
p=Path(os.environ['REVIEW_PACKET'])
public=p/'scratch/public/author-r3/receipts'
manifest={e['file']:e for e in json.loads((public/'MANIFEST.json').read_text())}
out={'groups':{},'srp':{},'owed':{},'fanout':{}}
for label in (sys.argv[1:] or ('A1','A8')):
 folder=p/'measurements'/label
 data=json.loads((folder/'results.json').read_text())
 for got in data['results']:
  name=got['group'];key=label+'/'+name
  expected=json.loads((public/'runs'/label/(name+'.json')).read_text())
  assert got==expected,key
  raw=(folder/(name+'.log')).read_bytes()
  digest=hashlib.sha256(raw).hexdigest()
  want=manifest['runs/'+key+'.log']['sha256']
  assert digest==want,(key,digest,want)
  out['groups'][key]={'grade_exact':True,'log_sha256':digest,'published_log_sha256':want}
  marks={};rxc=[];tails=[];passes=[];commits=collections.defaultdict(list);wires=collections.defaultdict(list)
  frame=None;endbyte=None;finish=None
  for line in raw.decode().splitlines():
   w=line.split()
   if not w:continue
   if w[0]=='MARK':marks[w[2]]=int(w[1])
   if w[0]=='RXS':frame=(int(w[2]),int(w[3]),w[4] if len(w)>4 else '-')
   if w[0]=='RXE':endbyte=int(w[1])
   if w[0]=='RXC':
    assert int(w[1])-endbyte==4,(key,w,endbyte)
    rxc.append((int(w[1]),int(w[2]),*frame))
   if w[0]=='PASS':
    passes.append((int(w[2]),int(w[4])))
    if ' W ' in line:
     tails.extend(tuple(int(s,16) if i else int(s) for i,s in enumerate(t.split(':'))) for t in line.split(' W ',1)[1].split())
   if w[0]=='TXC':commits[int(w[2])].append(int(w[1]))
   if w[0]=='WIRE':wires[int(w[3])].append((int(w[1]),int(w[2]),bytes.fromhex(w[4])))
   if w[0]=='SUMMARY':finish=int(dict(x.split('=') for x in w[1:])['sys'])
  if 'composed' in marks:
   start,stop=marks['composed'],marks['composed_end']
   total=0;records=[]
   # Contract channel 4 RX_TAIL: channel block base 0x100, stride 0x20, tail offset 4.
   tailword=(0x100+4*0x20+4)//4
   writes=[(c,v) for c,a,v in tails if a==tailword]
   for c,ch,interface,size,tag in rxc:
    if ch!=4:continue
    total+=2+(size+3)//4
    release=next((at for at,value in writes if value>=total),None)
    if start<=c<=stop:
     pass_end=next((s+2*n for s,n in passes if release is not None and s<=release<=s+2*n),None)
     records.append(dict(commit=c,release=release,end=pass_end,ms=((pass_end or finish)-c)/100000))
   assert len(records)==32,key
   left=sum(r['release'] is None or r['release']>stop for r in records)
   assert got['passes']['composed']['unreleased'].get('srp',0)==left
   source=[r for r in got['probes'] if '.service.srp.' in r['probe']]
   assert [round(r['ms'],5) for r in (records[0],records[-1])]==[r['ms'] for r in source],key
   out['srp'][key]=dict(committed=len(records),released_in_window=len(records)-left,first=records[0],last=records[-1])
   maximum=max(n for s,n in passes if start<=s<=stop)
   assert maximum==got['passes']['composed']['cycles'],key
  if name in ('backlog-owed','aecp-fanout'):
   decoded=[]
   for ch,frames in wires.items():
    assert len(commits[ch])==len(frames),(key,ch,len(commits[ch]),len(frames))
    decoded.extend((at,ch,i,f) for at,(_,i,f) in zip(commits[ch],frames))
   decoded.sort()
   if name=='backlog-owed':
    row=next(r for r in got['probes'] if r['probe']=='backlog.owed.if0')
    seqs=[int.from_bytes(f[62:64],'big') for at,ch,i,f in decoded if ch==1 and i==0 and row['start_sys']<at<=row['end_sys']]
    assert seqs==list(range(0x7380,0x7388)),(key,seqs)
    out['owed'][key]=dict(response_sequence_ids=[hex(s) for s in seqs],ms=row['ms'],from_room_ms=row['from_origin_ms'])
   else:
    rows=[]
    for row in got['probes']:
     if 'set_name' not in row['probe']:continue
     notifications=[(at,i,int.from_bytes(f[26:34],'big')) for at,ch,i,f in decoded if row['start_sys']<=at<=row['end_sys'] and ch==2 and len(f)>38 and f[36:38]==bytes.fromhex('8010')]
     count=16 if label=='A1' else 32
     assert len(notifications)==count and len(set((i,c) for _,i,c in notifications))==count,(key,notifications)
     assert max(at for at,_,_ in notifications)==row['end_sys']
     rows.append(dict(probe=row['probe'],recipients=count,ms=row['ms'],last_commit=row['end_sys']))
    out['fanout'][label]=rows
(p/'native-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:',len(out['groups']),'exact grades and raw log digests; SRP release/latency, seven owed responses, full capacity fan-out independently decoded')
