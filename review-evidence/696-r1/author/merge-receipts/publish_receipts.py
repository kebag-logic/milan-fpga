#!/usr/bin/env python3
"""Publish bounded, path-redacted receipts for the merged-head resume into merge-receipts/."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
work=Path(__file__).resolve().parent
packet=Path('<home>/milan-fpga-management/2026-09-23/696-a570')
dest=packet/'merge-receipts'
head=subprocess.check_output(['git','-C','<lane>','rev-parse','HEAD'],text=True).strip()
replacements=[
 ('<validation-tree>','<validation-tree>'),
 ('<parent-tree>','<parent-tree>'),
 (str(work/'docs'),'<gate-tree>'),
 (str(work),'<scratch>'),
 ('<field-generator>','<field-generator>'),
 ('<sdk>','<sdk>'),
 ('<lane>','<lane>'),
 ('python3','python3'),
 ('<doc-env>','<doc-env>'),
 ('<pinned-compiler>','<pinned-compiler>'),
 ('<synthesis-install>','<synthesis-install>'),
 ('<litex-env>','<litex-env>'),
 ('<home>','<home>'),
 ('<workspace>','<workspace>'),
]
provenance=[];large=[]
def digest(data):return hashlib.sha256(data).hexdigest()
def publish(source):
 raw=source.read_bytes();name=str(source.relative_to(work))
 entry=dict(source=name,raw_bytes=len(raw),raw_sha256=digest(raw))
 if len(raw)>=200000:
  entry['retention']='scratch only; exceeds packet size limit';large.append(entry);return
 text=raw.decode(errors='replace')
 for old,new in replacements:text=text.replace(old,new)
 text=re.sub(r'(?m)^(\| Host\s*:\s*).+$',r'\1<redacted>',text)
 cooked=text.encode();target=dest/name
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(cooked)
 entry.update(published=str(target.relative_to(packet)),published_bytes=len(cooked),published_sha256=digest(cooked))
 provenance.append(entry)
if dest.exists():shutil.rmtree(dest)
dest.mkdir()
def wanted(p):
 return p.suffix in ('.rc','.py','.sh','.txt','.jsonl','.patch') or p.name.endswith('.json') or (p.suffix=='.log' and (p.with_suffix('.rc').exists() or p.name.endswith(('-bank.log','-bank-merged.log','launch.log'))))
for p in sorted(work.glob('*')):
 if p.is_file() and wanted(p):publish(p)
for folder in ['parent-suites-logs','docs-merged','focus-merged','focus-merged/portability-results','route-queries','record','docs-final','focus-final','maap-ooc-dev','maap-ooc-merged']:
 root=work/folder
 if not root.exists():continue
 for p in sorted(root.glob('*')):
  if p.is_file() and (wanted(p) or p.suffix in ('.log','.rpt','.result','.tcl')):publish(p)
shipping=work/'shipping'
for p in sorted(shipping.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(shipping)
 top=p.parent==shipping and (p.suffix in ('.rc','.log') or p.name.endswith('.json'))
 rpt=p.suffix=='.rpt' and p.parent.name in ('gateware','ax7101-ooc','ax8x8-ooc')
 meas=p.name in ('baseline_integrated.tcl','baseline_ooc.tcl','baseline_images.json','baseline.log','baseline_parameters.json','baseline_chparam.txt','baseline_cells.tsv','baseline_scope_timing.tsv','rtl.tcl') and p.parent.name in ('gateware','ax7101-ooc','ax8x8-ooc','ax8x8-rtl')
 big=p.suffix=='.dcp'
 if top or rpt or meas or big:publish(p)
indexes=[]
for start in range(0,len(provenance),50):
 target=dest/f'PROVENANCE-{start//50+1:03d}.json'
 payload=json.dumps({'receipts':provenance[start:start+50]},indent=2)+'\n'
 assert len(payload.encode())<200000
 target.write_text(payload);indexes.append(str(target.relative_to(packet)))
(dest/'PROVENANCE.json').write_text(json.dumps({'packet_head':head,'receipt_indexes':indexes,'receipt_count':len(provenance)},indent=2)+'\n')
(dest/'SCRATCH-ARTIFACTS.json').write_text(json.dumps({'packet_head':head,'artifacts':large},indent=2)+'\n')
for f in packet.rglob('*'):
 if f.is_file():assert f.stat().st_size<200000,f
leak=[str(f) for f in dest.rglob('*') if f.is_file() and re.search(rb'/home/|<workspace>|alexandre|hackerman',f.read_bytes())]
print(f'Published {len(provenance)} bounded receipts; indexed {len(large)} raw artifacts; residual path/account matches: {leak[:10]}')
