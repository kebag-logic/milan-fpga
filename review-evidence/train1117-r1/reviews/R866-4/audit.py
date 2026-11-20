#!/usr/bin/env python3
"""Audit published receipt hashes, frozen merges and CPU table arithmetic."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
E = OUT / 'scratch/evidence/review-evidence/train1117-r1'
A = E / 'author-r6'
def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', *args])

manifest = json.loads((E / 'MANIFEST.json').read_text())
rows = [r for r in manifest if r['file'].startswith('author-r6/')]
for r in rows:
    assert hashlib.sha256((E/r['file']).read_bytes()).hexdigest() == r['published_sha256'], r['file']
print('Published manifest: verified', len(rows), 'author-r6 files; no reviewer reports opened')
for merge, frozen, shared in [
    ('c05d5acb','a16899b1', {'sw/firmware/ctrl/aecp/README.md','sw/firmware/ctrl/test/test_aecp.cpp'}),
    ('4b9f66c5','f09d82e0', {'docs/design/MAILBOX_SPLIT.md','docs/design/SPLIT_CONTROL_MEMORY.md',
                            'tb/verilator/ctrl_service_budget/README.md'})]:
    first, second = git('rev-parse',merge+'^1',merge+'^2').decode().splitlines()
    assert second == git('rev-parse',frozen).decode().strip()
    subprocess.run(['git','merge-base','--is-ancestor',second,'HEAD'],check=True)
    base=git('merge-base',first,second).decode().strip()
    paths=git('diff','--name-only',base,second).decode().splitlines()
    for path in paths:
        if path not in shared:
            assert git('diff',base,second,'--',path)==git('diff',first,merge,'--',path), path
        else:
            content=git('show',merge+':'+path).decode().splitlines()
            for side in (first,second):
                patch=git('diff','--unified=0',base,side,'--',path).decode().splitlines()
                added=[x[1:] for x in patch if x.startswith('+') and not x.startswith('+++')]
                assert all(x in content for x in added),path
    auto=git('merge-tree','--write-tree',first,second).decode().splitlines()[0]
    assert auto == git('rev-parse',merge+'^{tree}').decode().strip()
    print('Frozen merge',merge,second,'verified:',len(paths)-len(shared),'exact file patches;',len(shared),
          'shared files preserve both additions; complete tree equals clean merge')

for table, point, section in [('CPU-TABLE-8c5e2b4f.md','1x1/1if','step16/measure/out/survey-1x1'),
                              ('CPU-TABLE-92de01f7.md','8x8/1if','step15/measure/out/survey-8x8-1if')]:
    text=(A/table).read_text().split('## '+point+'\n')[1].split('\n## ')[0]
    ordinary=json.loads((A/'receipts'/section/'ordinary-costs/costs.json').read_text())['_most_cycles']
    count=0
    for line in text.splitlines():
        c=[x.strip() for x in line.split('|')]
        if len(c)<8 or not c[2].replace(',','').isdigit():continue
        key=c[1]; cycles=int(c[2].replace(',','')); rule=int(c[4]); stated=int(c[5])
        expected=((cycles*105+49999)//50000)*5
        assert rule==expected,(key,cycles,rule,expected)
        assert stated>=rule,(key,stated,rule)
        if key in ordinary:assert cycles==ordinary[key],(key,cycles,ordinary[key])
        count+=1
    assert count==68,count
    print(point,':',count,'statements recomputed; 0 exceeded; recorded cycle maxima agree with survey JSON')
    long=json.loads((A/'receipts'/section/'long-costs/costs.json').read_text())['_most_cycles']
    print('Long notice cycles:',long.get('item.aecp_long'),'; rule',((long['item.aecp_long']*105+49999)//50000)*5)

print('8c5e2b4f..HEAD changed paths:',git('diff','--name-only','8c5e2b4f','HEAD').decode().strip())
print('Archive commit signature status:',git('show','--no-patch','--format=%G?','563c16e5').decode().strip(),
      '(N = no Git signature; checksums prove contents, not signer identity)')
