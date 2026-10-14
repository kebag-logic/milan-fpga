#!/usr/bin/env python3
"""Verify published receipt hashes and grouped source-function coverage."""
import ast
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
commit='faf4ddda73e3a9ce91e1e6f35021af316ec6bdf6'
prefix='review-evidence/737-image-r1/'
def raw(name):
 return subprocess.check_output(['git','show',commit+':'+prefix+name],cwd=root)
def public(name):return json.loads(raw('author-r2/'+name))
manifest=json.loads(raw('MANIFEST.json'))
checked=[]
for row in manifest:
 if not row['file'].startswith('author-r2/') or row['file'].endswith('.md'):continue
 actual=hashlib.sha256(raw(row['file'])).hexdigest()
 assert actual==row['published_sha256'],row['file']
 checked.append({'file':row['file'],'sha256':actual,'published_digest_verified':True,'path_redacted':row['path_redacted']})
(out/'public-evidence-verification.json').write_text(json.dumps({'commit':commit,'verified':len(checked),'files':checked},indent=2)+'\n')
source=(root/'sw/builder/test_builder.py').read_bytes()
sha=hashlib.sha256(source).hexdigest()
main=next(n for n in ast.parse(source).body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'")
loop=next(n for n in main.body if isinstance(n,ast.For) and ast.unparse(n.target)=='fn')
expected=[n.id for n in loop.iter.elts]
actual=[];groups=[]
for i in range(9):
 row=public(f'builder-functions-{i}.json')
 names=[r['name'] for r in row['results']]
 assert row['source_sha256']==sha and row['require_rv32'] and row['group']==i
 assert names==row['groups'][i] and [n for g in row['groups'] for n in g]==expected
 receipt='builder-home-background.receipt.json' if i==1 else f'builder-group-{i}-0.receipt.json'
 result=public(receipt);assert result['rc']==0
 actual+=names
 groups.append({'group':i,'functions':names,'source_sha256':sha,'receipt':receipt,'rc':0})
assert collections.Counter(actual)==collections.Counter(expected)
assert len(expected)==len(set(actual))==103
(out/'builder-coverage.json').write_text(json.dumps({'source_sha256':sha,'expected':len(expected),'returned':len(actual),'exactly_once':True,'groups':groups,'origin':'published author evidence at '+commit+'; no reviewer builder execution'},indent=2)+'\n')
print(f'PASS: {len(checked)} published hashes; 103 invocations exactly once across nine successful groups at the exact source hash')
