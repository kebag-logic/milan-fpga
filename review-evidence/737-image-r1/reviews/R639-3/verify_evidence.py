#!/usr/bin/env python3
"""Independently compare public execution records with exact-head authorities."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve(); packet=Path(__file__).resolve().parent
public=packet/'scratch/public'
read=lambda n:json.loads((public/n).read_text())
lock=json.loads((root/'ci/image/image.lock.json').read_text())
cold=read('round3-cold-comparison.json')['cold_builds']
for name in ('a','b'):
 r=cold[name]; receipt=read(f'round3-{name}-validation-tools.receipt.json')
 for key,value in receipt.items(): assert r[key]==value
 for key in ('image_digest','image_id'): assert r[key]==lock[key]
 assert r['recipe_sha256']==lock['recipe_digest']
 rows=lock['base_layers']+lock['layers']
 assert r['layers']==[x['oci_digest'] for x in rows]
 assert r['diff_ids']==[x['diff_id'] for x in rows]
 metadata=read(f'round3-{name}-validation-tools.metadata.json')
 args=metadata['buildx.build.provenance']['invocation']['parameters']['args']
 assert 'no-cache' in args and args['force-network-mode']=='none'
 assert metadata['containerimage.digest']==lock['image_digest']
 assert 'containerimage.config.digest' not in metadata
for key in ('image_digest','image_id','layers','diff_ids','recipe_sha256'):
 assert cold['a'][key]==cold['b'][key]
source=(root/'sw/builder/test_builder.py').read_bytes()
source_hash=hashlib.sha256(source).hexdigest()
tree=ast.parse(source)
main=next(n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'")
loop=next(n for n in main.body if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='fn')
expected=[n.id for n in loop.iter.elts]
results=[]; partition=None; groups=[]
for i in range(9):
 row=read(f'builder-functions-{i}.json')
 assert row['source_sha256']==source_hash
 if partition is None: partition=row['groups']
 assert row['groups']==partition and row['group']==i and row['require_rv32']
 names=[v['name'] for v in row['results']]
 assert names==partition[i]
 receipt=read('builder-home-background.receipt.json') if i==1 else read(f'builder-group-{i}.json')[0]
 assert receipt['rc']==0 and '--require-rv32' in receipt['command']
 results.extend(names)
 groups.append({'group':i,'count':len(names),'rc':0,'skips':row.get('recorded_skips',[])})
assert Counter(results)==Counter(expected) and max(Counter(results).values())==1
assert [n for g in partition for n in g]==expected
smoke=read('round3-smoke.json')[0]
assert smoke['rc']==0 and '--network' in smoke['command']
assert smoke['command'][smoke['command'].index('--network')+1]=='none'
assert lock['image_digest'] in smoke['command']
smoke_log=(public/'round3-smoke-0.log').read_text()
assert 'PASS: all image tool families' in smoke_log and '3.12.3' in smoke_log
hosted=json.loads((packet/'scratch/hosted-job.json').read_text())
assert hosted['head_sha']=='fa8209889411e8ca95757174c981f720dbcd95a2' and hosted['name']=='docs-check'
lines=(packet/'scratch/hosted-docs.log').read_text().splitlines()
selected=[line for line in lines if ('Version: 20261004.327.1' in line or 'SKIP: the MAKEFLAGS += -e mutation:' in line)]
assert len(selected)>=2
runner=(packet/'scratch/runner-manifest.md').read_text()
make_line=next(line for line in runner.splitlines() if '| make ' in line)
pins=json.loads((root/'ci/image/sources.lock.json').read_text())
snapshots=read('round3-snapshots.json')
assert snapshots['rc']==0
locked={r['tool']:r for r in pins['packages'] if r.get('fallback_urls')}
assert len(locked)==len(snapshots['packages'])==185
for row in snapshots['packages']:
 target=locked[row['tool']]
 assert row['sha256']==target['sha256'] and row['size']==target['size'] and row['url'] in target['fallback_urls']
make_version=next(r['version'] for r in pins['packages'] if r['tool']=='make')
assert make_version in make_line
assert 'make\\t'+make_version in smoke_log and 'GNU Make 4.3' in smoke_log
summary={'cold_builds':{'same_manifest_config_all_14_layers':True,'manifest':lock['image_digest'],
 'config':lock['image_id'],'build_ms':[cold[n]['build_ms'] for n in ('a','b')],
 'size_bytes':cold['a']['size_bytes'],'missing_buildx_config_metadata_handled':True,
 'buildx':read('round3-buildx.json')['buildx_version']},
 'builder':{'source_sha256':source_hash,'exact_invocation_cover':len(expected),'groups':groups,
 'evidence_kind':'Historical grouped author execution on prior image; unchanged builder source; no manager source bank.'},
 'smoke':{'rc':smoke['rc'],'elapsed_ms':smoke['elapsed_ms'],'offline':True,'reference_python':'3.12.3',
 'kind':'Published author execution, not reviewer container execution.'},
 'retained_packages':{'published_downloads_checked_against_lock':185,'rc':0},
 'make_skip':{'job_url':hosted['html_url'],'head':hosted['head_sha'],'excerpts':selected,
 'runner_manifest':'https://github.com/actions/runner-images/blob/ubuntu24/20261004.327/images/ubuntu/Ubuntu2404-Readme.md',
 'runner_make':make_line,'image_make':make_version,'same_skip':True}}
(packet/'evidence-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS: cold identities, no-cache settings, config-key portability, 103-function exact cover, offline smoke record, hosted make version and skip.')
