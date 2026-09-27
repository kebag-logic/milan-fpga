"""Summarize capture integrity, readback deltas, and bounded MSRP bursts."""
from pathlib import Path
import collections,json,re,statistics,sys
from wire_summary import records
p=Path(__file__).resolve().parent.parent
def word(path,addr):
 t=path.read_text()
 m=re.search(r'^'+re.escape(addr)+r'  ((?:[0-9a-f]{2} ){3}[0-9a-f]{2})',t,re.M)
 assert m,(path,addr)
 return int.from_bytes(bytes.fromhex(m[1]),'little')
def max_window(times):
 left=0;largest=0
 for right,t in enumerate(times):
  while times[left]<=t-1000000000:left+=1
  largest=max(largest,right-left+1)
 return largest
out={}
for direction in ['listener','talker']:
 cycles=[]
 for f in sorted(p.glob(direction+'-[0-9][0-9][0-9]/analysis.json')):
  a=json.loads(f.read_text());d=f.parent
  bysender=collections.defaultdict(list);anchors=[];previous=None;reversals=0
  for r in records('/tmp/a386/'+d.name+'/tap.pcap'):
   anchors.append((r['host_ns']-r['tap_ns'])/1e9)
   if previous is not None and r['tap_ns']<previous:reversals+=1
   previous=r['tap_ns']
   fr=r['frame'];et=int.from_bytes(fr[12:14],'big')
   if et==0x8100:et=int.from_bytes(fr[16:18],'big')
   if et==0x22ea:
    sender='DUT' if r['port']==3 else 'bridge'
    bysender[sender].append(r['tap_ns']);bysender['combined'].append(r['tap_ns'])
  cs={}
  for side in ['before','after']:
   path=d/('console-'+side+'.txt')
   cs[side]={addr:word(path,addr) for addr in ['0x90000650','0x9000069c','0x900006b0','0x90000930','0x90000720']}
  assert all(cs[s][addr]==0 for s in cs for addr in ['0x90000650','0x9000069c','0x900006b0'])
  assert all(cs[s]['0x90000720']==1 for s in cs)
  x,y=[cs[s]['0x90000930'] for s in ['before','after']]
  diag=dict(tx_delta=((y>>16)-(x>>16))&65535,rx_delta=((y&255)-(x&255))&255,drops_before=(x>>8)&255,drops_after=(y>>8)&255)
  assert diag['drops_before']==diag['drops_after']==0
  assert '0 packets dropped by kernel' in (d/'capture.txt').read_text()
  c=dict(name=d.name,clock_anchor_range_s=max(anchors)-min(anchors),timestamp_reversals=reversals,max_msrp_pdus_one_second={s:max_window(sorted(ts)) for s,ts in bysender.items()},processor=diag)
  (d/'integrity.json').write_text(json.dumps(c,indent=2)+'\n')
  cycles.append(c)
 if cycles:
  out[direction]=dict(cycles=len(cycles),max_clock_anchor_range_s=max(c['clock_anchor_range_s'] for c in cycles),timestamp_reversals=sum(c['timestamp_reversals'] for c in cycles),max_msrp_pdus_one_second={s:max(c['max_msrp_pdus_one_second'].get(s,0) for c in cycles) for s in ['DUT','bridge','combined']},processor_tx_delta=sum(c['processor']['tx_delta'] for c in cycles),processor_rx_mod256_sum=sum(c['processor']['rx_delta'] for c in cycles),drops=0)
(p/'integrity-summary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
