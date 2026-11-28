#!/usr/bin/env python3
"""Verify public receipt bindings and independently recompute the held and wire bounds."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
public = packet/'scratch/public/review-evidence/usbnet-r1'
r7 = public/'author-r8/round7/receipts'
r8 = public/'author-r8/round8/receipts'
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(ref, path): return subprocess.check_output(['git','-C',str(root),'show',ref+':'+path])
out = {}
identity = read(r8/'identity.json')
out['dependency_files'] = [dict(path=x['path'], match=sha(root/x['path']) == x['sha256'] and (root/x['path']).read_bytes() == blob('640699e6',x['path'])) for x in identity['dependency_files']]
out['firmware_source_delta'] = subprocess.check_output(['git','-C',str(root),'diff','--name-only','640699e6..HEAD','--','sw/firmware','configs'],text=True).splitlines()
out['gitlink_delta'] = [l for l in subprocess.check_output(['git','-C',str(root),'diff','--raw','640699e6..HEAD'],text=True).splitlines() if '160000' in l]
out['firmware'] = []
for row in identity['firmware']:
    directory = r8/'firmware'/row['tree']/row['recipe']
    out['firmware'].append(dict(recipe=row['recipe'],side=row['tree'],published_elf_sha256=row['hashes']['ctrl_app.elf'],elf_bytes_published=(directory/'ctrl_app.elf').exists(),map_header_matches=sha(directory/'ctrl_plat_map_gen.h') == row['hashes']['ctrl_plat_map_gen.h']))
chain = r7/'shipping-chain/egress-controls-named'
meta = read(chain/'chain.json')
out['shipping_chain'] = {'source_matches':{n:sha(root/n)==s for n,s in meta['sources'].items()},'generated_rtl_matches':sha(chain/'usbnet_egress_chain.v')==meta['verilog_sha256']}
handshake=[tuple(map(int,l.split()[1:])) for l in (chain/'handshake.log').read_text().splitlines() if l.startswith('HANDSHAKE ')]
out['handshake']={'cases':len(handshake),'complete':{x[:3] for x in handshake}=={(l,d,e) for l in (14,60,64,90,127,512,1514,1515) for d in range(8) for e in range(8)},'maximum_ps':max(x[-1] for x in handshake)}
sys.path.insert(0,str(root/'tb/verilator/usbnet'))
import egress_grade, egress_usb
archive={x['case']:x for x in read(r7/'census/ARCHIVE.json')['cases']}
completed={x['variant']+'/'+x['group']:x for x in read(r7/'census/completed.json')}
bound=read(r8/'egress-evidence-identity.json')
rows={}
errors=[]
for item in bound['cases']:
    case=item['case']; receipt=r7/'egress-cases'/(case+'.json'); data=read(receipt)
    if sha(receipt)!=item['replay_receipt_sha256']: errors.append([case,'receipt hash'])
    if not item['trace_sha256']==data['trace_sha256']==archive[case]['raw_sha256']==completed[case]['trace_sha256']: errors.append([case,'trace binding'])
    if data['inputs']!=bound['sources']: errors.append([case,'inputs'])
    rows[case]=data['result']
out['wire_sources']={n:sha(root/n)==s for n,s in bound['sources']['sources'].items()}
p=egress_usb.base.params(egress_usb.base.arty_spec())
ok,lines=egress_grade.verdict(rows,p)
out['wire']={'cases':len(rows),'images':len({k.split('/')[0] for k in rows}),'archive_cases':len(archive),'completed_cases':len(completed),'binding_errors':errors,'verdict':ok,'lines':lines,'largest_wait_ps':max(x['wait_ps'] for x in rows.values()),'raw_traces_published':sum((r7/'census'/x['path']).exists() for x in archive.values()),'departure_disagreements':sum(x['agree_ps']!=0 for x in rows.values())}
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import egress_ledger
out['ledger']={'original':egress_ledger.LEDGER['arty-1x1'],'usb':egress_ledger.LEDGER['arty-usbnet-1x1']}
for point,expected in [('arty-usbnet-1x1',0),('arty-1x1',1)]:
    paths=sorted((r8/'census').glob('*/results'))
    cmd=['python3','-B',str(root/'tb/verilator/ctrl_service_budget/egress_ledger.py'),'--point',point,*map(str,paths)]
    r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    name='retained-'+point
    (packet/(name+'.log')).write_text(r.stdout.replace(str(packet),'$REVIEW_PACKET').replace(str(root),'$REVIEW_ROOT'))
    (packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
    out['ledger'][point+'_returncode']=r.returncode
    assert r.returncode==expected
spec=importlib.util.spec_from_file_location('usb_plants',root/'tb/verilator/usbnet/mutants.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
out['plants']=[]
for name,harness,file,old,new,want in module.CONTROLS:
    log=(r7/'plants'/(name+'.log')).read_text()
    named=any(l.startswith('FAIL ') and '.cpp:' in l and want in l for l in log.splitlines())
    out['plants'].append(dict(name=name,named_failure=named,current_anchor_count=(root/'hdl/usbnet'/file).read_text().count(old)))
out['acmp_composition']={'current_service_ms':29.84,'additional_us':3046/80,'total_ms':29.84+3046/80000,'margin_us':(30-29.84-3046/80000)*1000,'published_old_service_ms':29.77,'published_old_total_ms':29.808075,'published_old_margin_us':191.925}
(packet/'receipt-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('plants','firmware','ledger')},indent=2))
print('Plants:',len(out['plants']),'named failures:',sum(x['named_failure'] for x in out['plants']))
