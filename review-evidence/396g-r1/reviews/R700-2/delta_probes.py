#!/usr/bin/env python3
"""Independent boundary captures from the documented layout; no source edits."""
import hashlib, importlib.util, json, pathlib, struct, sys
repo=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_delta',repo/'tb/tools/torture_campaign.py')
t=importlib.util.module_from_spec(spec);sys.modules[spec.name]=t;spec.loader.exec_module(t)
N=8192; C=4; RATE=48000
arms=[dict(index=i,**fields) for i,fields in [
 (100,{'class':'dropped','n':3}),(300,{'class':'repeated','n':2}),
 (500,{'class':'bit-flip','mask':256,'channel':1}),
 (7492,{'class':'dropped','n':3}),(7742,{'class':'repeated','n':2}),
 (7992,{'class':'bit-flip','mask':256,'channel':3})]]
def word(tag,n):
 code=(n//2048*0x9e3779b1)&0xffffffff
 return ((tag<<12)|((n%2048)<<1)|((code>>(n%32))&1))<<8
def capture(ops=(),frames=N):
 data=[]
 for i in range(frames):
  shift=sum(a.get('n',0)*(1 if a['class']=='dropped' else -1)
            for a in arms if a['class'] in ('dropped','repeated') and a['index']<=i)
  shift+=sum(op[2] for op in ops if op[0]=='shift' and op[1]<=i)
  row=[word(c+1,i+shift) for c in range(C)]
  for a in arms:
   if a['class']=='bit-flip' and i==a['index']:row[a['channel']]^=a['mask']
  for op in ops:
   if op[0]=='xor' and op[1]<=i<op[1]+op[2]:row[op[3]]^=op[4]
   if op[0]=='swap' and op[1]<=i<op[1]+op[2]:
    a,b=op[3:5];row[a],row[b]=row[b],row[a]
  data.append(struct.pack('>4I',*row))
 return b''.join(data)
rows=[]
def probe(name,ops=(),frames=N,losses=(),chunk=None,steps=()):
 b=capture(ops,frames)
 span=(frames+sum(l['frames'] for l in losses))/RATE
 layout=t.CounterCapture(C,'big',RATE,100.,200.,anchors=((frames,100.+span,200.+span),),gptp_steps_wall_s=steps)
 data=b if chunk is None else [b[i:i+chunk] for i in range(0,len(b),chunk)]
 verdict,detail=t.grade_audio_counter_capture(data,layout,t.CounterRunLog(arms,list(losses),0))
 row=dict(name=name,ops=ops,frames=frames,chunk=chunk,verdict=verdict,
          sha256=hashlib.sha256(b).hexdigest(),missed=detail.get('planted_missed'),
          counts=detail.get('counts'),why=detail.get('why'),timing_unsupported=detail.get('timing_unsupported'),
          events=[e for e in detail.get('events',[]) if e['attribution']!='planted'])
 rows.append(row)
 print(name,verdict,[(e['channel'],e['capture_index'],e['class'],e.get('n'),e.get('mask'),e.get('unresolved')) for e in row['events']],flush=True)
 return row
probe('clean-control')
for n in (3000,4096,8192,409600,-3000,-4096):probe('interior-slip-'+str(n),[('shift',3000,n)])
for at,n in ((8191,2048),(8190,8192),(8191,4096)):
 probe('tail-slip-%d-%d'%(at,n),[('shift',at,n)])
probe('tail-slip-with-64-more-frames',[('shift',8191,2048)],frames=N+64)
probe('tail-slip-chunked',[('shift',8191,2048)],chunk=113)
probe('initial-slip',[('shift',10,4096)])
for n in (2,63,64,65,100):probe('constant-code-xor-'+str(n),[('xor',3000,n,2,256)])
probe('constant-code-xor-chunked',[('xor',3000,100,2,256)],chunk=113)
probe('tag-bit-flip',[('xor',3000,1,0,0x200000)])
probe('static-swap',[('swap',0,N,0,2)])
probe('hold',[('shift',3000,-1),('shift',3001,1)])
probe('capture-gap-clocks',[('shift',2000,409600),('xor',3000,1,0,1)],losses=[dict(index=2000,frames=409600)])
probe('capture-gap-gptp-step',[('shift',2000,409600),('xor',3000,1,0,1)],losses=[dict(index=2000,frames=409600)],steps=(105.,))
items=list(t.RELEASE_PERSISTED_ITEMS);pre=dict.fromkeys(items,'old');new=dict.fromkeys(items,'new');defaults=dict.fromkeys(items,'default')
for name,post,pending,window,cut in [('new-in-window',new,new,(40,41),40),('old-in-window',pre,new,(40,41),40.5),
 ('all-default-pending',defaults,defaults,(40,41),40.5),('one-default-pending',new,dict(new,**{items[0]:'default'}),(40,41),40.5),
 ('cut-at-end',new,new,(40,41),41),('cut-before-start',new,new,(40,41),39),
 ('mixed-readback',dict(pre,**{items[0]:'new'}),new,(40,41),40.5)]:
 result=t.check_release_state_restored(pre,post,defaults,items=items,phase='journal_commit',committed=t.ReleaseCommitCut(pending,window,cut))
 rows.append(dict(name=name,result=result));print(name,result,flush=True)
names=t.RELEASE_ZERO_GROWTH_COUNTERS+('MEDIA_UNLOCKED',)
for name,times,values in [('inside-window',(0,10,20,60),(0,0,1,1)),('after-window',(0,10,20,60),(0,0,0,1)),('ambiguous-read',(0,60),(0,1))]:
 reads=[dict(target='input-0',timestamp_s=s,values=dict(dict.fromkeys(names,0),MEDIA_UNLOCKED=v)) for s,v in zip(times,values)]
 result=t.check_release_soak_counters(reads,[dict(target='input-0',kind='planted',window_s=(10,20))],targets=['input-0'],capture_complete=True)
 rows.append(dict(name=name,result=result));print(name,result,flush=True)
(out/'delta-probes.json').write_text(json.dumps(dict(period_frames=2**43,period_days_at_192k=2**43/192000/86400,
 run_frames_at_192k=86400*192000,probes=rows),indent=2)+'\n')
