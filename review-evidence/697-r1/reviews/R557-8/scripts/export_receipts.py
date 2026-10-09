#!/usr/bin/env python3
import hashlib,json,pathlib,shutil,sys
r=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();s=p/'scratch';d=p/'receipts';rows=[]
replacements=[(str(p),'$PACKET'),(str(r),'$SOURCE'),('<home-path>/work/tsn-c-stack/tsn-c-stack','$HOSTED_SOURCE'),('<home-path>','$HOSTED_HOME'),(str(pathlib.Path.home()),'$HOME'),(str(r.parents[1]),'$WORKSPACE')]
def copy(src,dst):
 if not src.is_file():return
 raw=src.read_bytes();text=raw.decode()
 for before,after in replacements:text=text.replace(before,after)
 data=text.encode();dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
 rows.append(dict(file=dst.relative_to(p).as_posix(),original_sha256=hashlib.sha256(raw).hexdigest(),published_sha256=hashlib.sha256(data).hexdigest(),location_redacted=raw!=data))
def globs(src,dst,patterns):
 for pattern in patterns:
  for f in sorted(src.glob(pattern)):copy(f,dst/f.relative_to(src))
local=s/'local';out=d/'local'
globs(local,out,['*.log','*.rc','gates.json','templates/*.log','templates/*.xml','conditionals/results.json','conditionals/**/*.log','dependencies/*.log','dependencies/campaign/results.json','dependencies/campaign/message-markers.json','dependencies/campaign/*/*.xml','graphs/*.svg','rv32/results.json','rv32/*/*.log','rv32/*/*.map','rv32/*/CMakeFiles/rv32_smoke.dir/link.txt','mutations/results.json','mutations/message-markers.json','mutations/*/*.xml','mutations/*/*.log'])
for name in ['package-prefix-probe','round8-replay','replays']:
 src=s/name;dst=d/name
 globs(src,dst,['*.log','*.rc','*.json','flags.txt'])
globs(s/'package-prefix-probe',d/'package-prefix-probe',['dependency/*.log','mutation/results.json','mutation/message-markers.json','mutation/*/*.xml','system-header-control/results.json','system-header-control/message-markers.json','system-header-control/*/*.xml'])
globs(s/'round8-replay',d/'round8-replay',['assertions/*.json','comments/*.json','spi-tree/*.log','dependencies/*.log'])
globs(s/'replays',d/'replays',['r5566/probes.json','r5564/*.json','r5576-controls/*.json','r5565-hidden/*.json','r5574-comments/*.json','legacy5/receipts/*.json','legacy6/receipts/*.json','early/receipts/*.json','r5565-tree/*.log','early-gates/*.log','early-driver/*.log'])
for run in [37925745383,37925739153]:
 src=s/('hosted-'+str(run));dst=d/('hosted-'+str(run))
 globs(src,dst,['quality-evidence/*.log','quality-evidence/*.rc','quality-evidence/gates.json','quality-evidence/mutations/results.json','quality-evidence/mutations/message-markers.json','quality-evidence/mutations/*/*.xml','rv32-evidence/results.json','rv32-evidence/*/*.log'])
copy(s/'setup-sdk.log',d/'setup-sdk.log')
globs(s/'assertion-audit',d/'assertion-audit',['*.log'])
copy(s/'hosted-checks-latest.txt',d/'hosted-checks.txt')
# Normalize reviewer JSON receipts whose original files were generated directly into receipts.
for name in ['assertion-audit.json','hosted-audit.json']:
 src=d/name
 if src.exists():copy(src,src)
(p/'receipts/receipt-format.json').write_text(json.dumps(dict(policy='Only location prefixes are replaced in published text. Original compiler, test and probe outputs remain under unpublished scratch. No result, measurement or failure text is changed. Per-arm audits are regenerated against the published XML.',files=rows),indent=2)+'\n')
print(len(rows),'text receipts exported')
