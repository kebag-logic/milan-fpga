#!/usr/bin/env python3
"""Observe all refusal terms and cross-grade four omissions on three shapes."""
import argparse,collections,concurrent.futures,dataclasses,json,os,pathlib,re,sys,tempfile,time
ap=argparse.ArgumentParser();ap.add_argument('root',type=pathlib.Path);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
ROOT=a.root.resolve();P=pathlib.Path(__file__).resolve().parents[1]
os.environ['TMPDIR']=str(P/'scratch');sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as t
import read_fault_cases as r
firmware=t.FIRMWARE.read_text();start=time.monotonic()
anchor='\treturn rd;\n}\n\n/* Whether two refused reads'
replacement='\tprintf("TERMS %lu %u %lu %lu %lu\\n", (unsigned long)(slot == NVM_SLOT_A ? 0u : 1u), (unsigned)rd.vd, (unsigned long)rd.bytes, (unsigned long)rd.digest, (unsigned long)rd.tail);\n'+anchor
assert firmware.count(anchor)==1
instrumented=firmware.replace(anchor,replacement)
rows=[]
with tempfile.TemporaryDirectory(dir=P/'scratch',prefix='term-probe-') as tmp:
 for shape in ['endstation_arty_4x4',*r.PRODUCT_SHAPES]:
  w=pathlib.Path(tmp)/shape;w.mkdir()
  b=t.make_bench(ROOT/'configs'/f'{shape}.yaml',w,firmware)
  cases=[c for c in r.fault_cases(t.KLJ2_HDR+(b.img_len-t.KLJ2_HDR-t.KLJ2_TRAILER)//2) if r.term_of(c)]
  assert len(cases)==128
  census=collections.Counter(r.term_of(c) for c in cases);assert set(census.values())=={32}
  print(shape,'term census',dict(census),flush=True)
  ib=t.replant(b,w/'instrumented',instrumented);fr=t.fault_run(ib)
  for n,c in enumerate(cases):
   newer=fr.containers[(c.seq,False)]
   other=fr.containers[(c.seq,True)] if c.older else b'\xff'*t.SLOT
   slots={c.valid:newer,c.other:other}
   fa=w/'a.bin';fb=w/'b.bin';fa.write_bytes(slots['a']);fb.write_bytes(slots['b'])
   opts=['--slot-a',str(fa),'--slot-b',str(fb)]
   opts+=['--boot','--idle-ms','100',*c.fault,'--restart'] if c.restart else [*c.fault,'--boot']
   out,_,_=t.run(ib,*opts)
   if c.restart:out=out.split('HOST restarting\n',1)[1].split('HOST restarted\n',1)[0]
   views=[list(map(int,m)) for m in re.findall(r'TERMS (\d+) (\d+) (\d+) (\d+) (\d+)',out)]
   slotcode=0 if c.fault[1][0]=='a' else 1
   views=[v[1:] for v in views if v[0]==slotcode][:3]
   term=r.term_of(c);index=[x[0] for x in r.COMPARISON].index(term)
   assert len(views)==3 and views[0][0]!=t.VD_OK and views[1][0]!=t.VD_OK and views[2][0]==t.VD_OK,(c,views)
   assert [i for i in range(4) if views[0][i]!=views[1][i]]==[index],(c,views)
   rows.append(dict(shape=shape,case=dataclasses.asdict(c),term=term,views=views,transcript=out))
  print(shape,'observed 128/128 term-isolated refusal pairs then clean reads',flush=True)
  for term,spelling,_ in r.COMPARISON:
   label=r.control_of(term);assert firmware.count(spelling)==1
   pb=t.replant(b,w/label,firmware.replace(spelling,'1'));pf=t.fault_run(pb)
   def one(pair):
    i,c=pair;cw=pb.work/f'case-{i}';cw.mkdir()
    return r.term_of(c),t.grade_fault_case(pb,pf,c,cw)
   with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:result=list(pool.map(one,enumerate(cases)))
   matrix={x[0]:sum(any(r.alone_in(x[0]) in f for f in fs) for ct,fs in result if ct==x[0]) for x in r.COMPARISON}
   assert matrix=={x[0]:32 if x[0]==term else 0 for x in r.COMPARISON},matrix
   assert all(not fs for ct,fs in result if ct!=term), 'off-class findings'
   print(shape,label,json.dumps(matrix,sort_keys=True),flush=True)
   (P/'receipts'/f'terms-{shape}-{label}.json').write_text(json.dumps([dict(term=ct,findings=fs) for ct,fs in result],indent=2)+'\n')
raw=json.dumps(rows,indent=2)+'\n'
(P/'scratch/term-views.raw.json').write_text(raw)
published=re.sub(re.escape(str(P/'scratch'))+r'/term-probe-[^/]+', '<probe>', raw)
(P/'receipts/term-views.json').write_text(published)
import hashlib
(P/'receipts/term-view-normalization.json').write_text(json.dumps(dict(rule='Only disposable absolute directory replaced with <probe>; observations unchanged',raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),published_sha256=hashlib.sha256(published.encode()).hexdigest()),indent=2)+'\n')
print('PASS: 384 observed term cases; 12 removal matrices; elapsed',round(time.monotonic()-start,2),flush=True)
