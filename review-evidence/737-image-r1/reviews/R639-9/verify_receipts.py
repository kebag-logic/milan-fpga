#!/usr/bin/env python3
"""Read-only verification of published evidence and the source it covers.
Run: python3 -B verify_receipts.py CHECKOUT PACKET
"""
import contextlib
import hashlib
import importlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

root, packet = (Path(s).resolve() for s in sys.argv[1:])
def load(path):
    return json.loads(path.read_text())
def sha(data):
    return hashlib.sha256(data).hexdigest()
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args], env={**__import__('os').environ, 'GIT_NO_REPLACE_OBJECTS':'1'})
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '6f86eee604729b80684526fc5b9be720d94f179a'
for x in load(packet/'evidence-verification.json')['files']:
    assert sha((packet/'evidence'/x['file']).read_bytes()) == x['published_sha256'], x['file']
inv = load(root/'ci/image/tool-inventory.json')
for path, expected in inv['inputs'].items():
    assert sha((root/path).read_bytes()) == expected, path
old = json.loads(git('show','1c4d722c:ci/image/tool-inventory.json'))
assert inv['tools'] == old['tools'] and inv['residue'] == old['residue']
sys.path[:0] = [str(root/'scripts'), str(root/'ci/image')]
import ci_differential
capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    assert ci_differential.check() == 0
import build
lock = load(root/'ci/image/image.lock.json')
assert build.recipe_digest() == lock['recipe_digest']
trace = load(root/'ci/image/exec-audit-receipt.json')
source = trace['source']['commit']
assert git('diff','--name-only',source,head).decode().splitlines() == ['ci/image/exec-audit-receipt.json']
assert git('rev-parse',source+'^{tree}').decode().strip() == trace['source']['tree']
assert trace['image'] == lock['image_digest']
assert trace['clean'] and trace['reached'] == 98 and trace['traced'] == 94
assert len(trace['steps']) == 94 and len({s['step'] for s in trace['steps']}) == 94
assert all(s['clean'] and s['exit_status'] == 0 and not s['findings'] for s in trace['steps'])
import audit_population
reached=audit_population.reached_steps(root)
reconciliation={r['step']:r for r in trace['reconciliation']}
assert len(reached)==98 and len(reconciliation)==98
for step in reached:
    key=f"{step['workflow']}#{step['job']}#{step['index']}"
    text, reason, removed=audit_population.image_form(step['name'],step['run'])
    row=reconciliation[key]
    assert row['traced'] == (text is not None),key
    if text is not None: assert row['text_sha256']==sha(text.encode()),key
summary=load(packet/'evidence/author-r9/round9-population-receipt.json')['committed_receipt']
assert sha((root/'ci/image/exec-audit-receipt.json').read_bytes()) == summary['sha256']
assert sum(s['instances'] for s in trace['steps']) == summary['instances'] == 183831
assert len(trace['commands']) == 115 and all(c['instances'] for c in trace['commands'])
assert sum(c['arguments']=='listed' for c in trace['commands']) == 111

names=load(root/'ci/image/exec-audit.json')
def variant(row):
    lines=(root/row['variant_of']).read_text().splitlines(keepends=True)
    diff=row['diff'].splitlines(keepends=True)
    out=[]; pos=0; i=2
    while i<len(diff):
        m=re.match(r'@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@',diff[i]); assert m,diff[i]
        start=int(m[1])-(m[2]!='0'); out.extend(lines[pos:start]); pos=start; i+=1
        while i<len(diff) and not diff[i].startswith('@@'):
            line=diff[i]; i+=1
            if line.startswith((' ','-')):
                assert lines[pos]==line[1:],(row['variant_of'],pos)
                pos+=1
            if line.startswith((' ','+')): out.append(line[1:])
    out.extend(lines[pos:]); return ''.join(out)
for key,row in names['inline_programs'].items():
    text=row.get('text') if 'text' in row else variant(row)
    assert sha(text.encode()) == key,key
    assert (root/row['source']).exists(),row['source']
for key,row in names['generated_programs'].items():
    assert re.fullmatch('[0-9a-f]{64}',key) and row['reason'] and (root/row['generator']).exists(),row
used={p.get('sha256') for s in trace['steps'] for p in s['population'] if p['provenance'] in ('pinned','generated')}
assert set(names['inline_programs']) <= used
# Generated rows omit their digest; complete generated-list use is author-reported, not proved here.
assert list(names['checkout_writes']) == ['tb/verilator/csr/Makefile']
final=load(packet/'evidence/author-r9/round9-final-checks.json')
assert final['head']==head and final['python']=='3.12.3'
assert len(final['checks'])==26 and all(c['rc']==0 for c in final['checks'])
assert final['checks'][-1]['check']=='inventory-check-last'
controls=(packet/'evidence/author-r9/round9-final-checks-logs/exec-audit-selftest-image.log').read_text()
assert sum(s.startswith('PASS:') for s in controls.splitlines())==74
out={'head':head,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'published_files_verified':len(load(packet/'evidence-verification.json')['files']),
     'inventory_input_digests':len(inv['inputs']),'unchanged_tools':len(inv['tools']),'unchanged_residue_entries':len(inv['residue']),
     'recipe_digest':lock['recipe_digest'],'image':lock['image_digest'],'differential_check':capture.getvalue().strip(),
     'trace_source':trace['source'],'only_trace_receipt_changed_since_source':True,'reached':98,'traced':94,
     'exec_instances':183831,'observed_commands':115,'listed_arguments':111,'selftest_pass_lines':74,'final_checks':26,
     'inventory_check_last':True,'inline_hashes_reconstructed':len(names['inline_programs']),
     'generated_source_references':len(names['generated_programs']),'all_inline_entries_observed':True,'generated_entry_use':'author-reported; aggregate rows omit digests',
     'limit':'Author execution evidence; read-only verification here. No signature or raw per-instance log authentication is implied.'}
print(json.dumps(out,indent=2))
