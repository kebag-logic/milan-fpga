#!/usr/bin/env python3
"""Collect public-safe receipts, retaining unredacted originals under scratch.
Usage: package_receipts.py CHECKOUT PACKET
"""
import hashlib
import json
import pathlib
import re
import shutil
import sys

root,packet=(pathlib.Path(p).resolve() for p in sys.argv[1:3])
ev=packet/'scratch/evidence/author-r4/receipts'
def publish(src,dst):
    text=src.read_text()
    text=text.replace(str(packet),'<packet>').replace(str(root),'<checkout>')
    text=re.sub(r'/tmp/mbx-selftest-[^/\s]+','<temporary-generator-directory>',text)
    (packet/dst).parent.mkdir(parents=True,exist_ok=True)
    (packet/dst).write_text(text)
if (packet/'ack-probe.log').exists() and not (packet/'scratch/ack-probe-original.log').exists():
    shutil.copyfile(packet/'ack-probe.log',packet/'scratch/ack-probe-original.log')
publish(packet/'scratch/ack-probe-original.log','ack-probe.log')
for src,dst in [('scratch/response-probe.log','response-probe.log'),
                ('scratch/delta-probes/if1.log','delta-probes-if1.log'),
                ('scratch/delta-probes/if2.log','delta-probes-if2.log'),
                ('scratch/generator.log','generator.log')]:
    publish(packet/src,dst)
for p in ['gates/fw-coverage-check.txt','export/export-digests.txt','images/linked-images.txt',
          'gates/census.txt','gates/mbx-make.txt','gates/mbx-mutants.txt']:
    publish(ev/p,'published/'+p)
mutants=[]
for p in sorted((ev/'aecp-mutants').glob('final-shard-*-results.json')):
    mutants+=json.loads(p.read_text())
images={p.name:json.loads(p.read_text()) for p in (ev/'images').glob('head-*.plan.txt')}
exports={p.name:json.loads(p.read_text()) for p in (ev/'export').glob('export-compare-*.json')}
doc= (ev/'gates/docs-gates.txt').read_text()
summary={'evidence_commit':'2d88c87ca36b521ac875b6299c2a3204040e942b',
         'firmware_execution_head':(ev/'fw/head.txt').read_text().strip(),
         'aecp_mutants':{'count':len(mutants),'caught':sum(x['caught'] for x in mutants),
                         'unique_names':len({x['name'] for x in mutants})},
         'docs':{'commands':len(re.findall(r'^\[rc=0\]',doc,re.M)),
                 'nonzero_commands':re.findall(r'^\[rc=[1-9].*$',doc,re.M),
                 'ending':doc.splitlines()[-2:]},
         'image_plans':images,
         'export_comparisons':{p:{k:v for k,v in d.items() if k in ['files','identical','different','missing']}
                               for p,d in exports.items()},
         'probe_source_sha256':{p:hashlib.sha256((packet/p).read_bytes()).hexdigest()
                                for p in ['response_probe.py','probe_ack.py']}}
(packet/'published-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['image_plans','export_comparisons']},indent=2))
