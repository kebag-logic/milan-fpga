"""Verify public receipt bytes and reconcile their source-bound assertions."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'ci/image')]
import audit_population
import ci_differential
import build

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

manifest = {row['file']: row for row in json.loads((PACKET / 'evidence/MANIFEST.json').read_text())}
tree = {row['path']: row for row in json.loads((PACKET / 'scratch/evidence-tree.json').read_text())['tree']}
checked = []
for path in sorted((PACKET / 'evidence').rglob('*')):
    if not path.is_file():
        continue
    relative = path.relative_to(PACKET / 'evidence').as_posix()
    data = path.read_bytes()
    blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    assert blob == tree['review-evidence/737-image-r1/' + relative]['sha'], relative
    if relative != 'MANIFEST.json':
        assert sha(data) == manifest[relative]['published_sha256'], relative
    checked.append({'file': relative, 'sha256': sha(data), 'git_blob': blob})
commit = json.loads((PACKET / 'evidence-commit.json').read_text())
signature_files = [p for p in tree if p.startswith('review-evidence/737-image-r1/') and
                   p.endswith(('.sig', '.asc', '.pub', '.pem'))]
assert ci_differential.check() == 0
receipt = json.loads((ROOT / 'ci/image/exec-audit-receipt.json').read_text())
reached = audit_population.reached_steps(ROOT)
keys = {f"{r['workflow']}#{r['job']}#{r['index']}" for r in reached}
reconciliation = {r['step']: r for r in receipt['reconciliation']}
assert keys == set(reconciliation)
assert {s['step'] for s in receipt['steps']} == {k for k,r in reconciliation.items() if r['traced']}
assert len(receipt['steps']) == 94
transforms = []
for step in reached:
    key = f"{step['workflow']}#{step['job']}#{step['index']}"
    text, why, removed = audit_population.image_form(step['name'], step['run'])
    row = reconciliation[key]
    assert row['traced'] == (text is not None), key
    if text is not None:
        assert row['text_sha256'] == sha(text.encode()), key
    transforms.append({'step': key, 'traced': row['traced'], 'why': why})
author = json.loads((PACKET / 'evidence/author-r8/round8-population-receipt.json').read_text())
assert sha((ROOT / 'ci/image/exec-audit-receipt.json').read_bytes()) == author['committed_receipt']['sha256']
assert receipt['source']['tree'] == git('rev-parse', receipt['source']['commit']+'^{tree}').decode().strip()
assert git('diff', '--name-only', receipt['source']['commit'], 'HEAD').decode().splitlines() == ['ci/image/exec-audit-receipt.json']
docs = json.loads((PACKET / 'evidence/author-r8/round8-population-docs-check.json').read_text())
assert sha((PACKET / 'evidence/author-r8/round8-population-docs-check.json').read_bytes()) == author['docs.json']['sha256']
assert len(docs['steps']) == 46 and all(s['clean'] and s['exit_status'] == 0 for s in docs['steps'])
final = json.loads((PACKET / 'evidence/author-r8/round8-final-checks.json').read_text())
assert final['head'] == git('rev-parse','HEAD').decode().strip()
assert len(final['checks']) == 26 and all(c['rc'] == 0 for c in final['checks'])
assert final['checks'][-1]['check'] == 'inventory-check-last'
inventory = json.loads((ROOT/'ci/image/tool-inventory.json').read_text())
previous = json.loads(git('show', 'feef7c9f:ci/image/tool-inventory.json'))
assert inventory['tools'] == previous['tools']
assert inventory['residue'] == previous['residue']
input_checks = {p: sha((ROOT/p).read_bytes()) == digest for p,digest in inventory['inputs'].items()}
assert all(input_checks.values())
names = json.loads((ROOT/'ci/image/exec-audit.json').read_text())
lock = json.loads((ROOT/'ci/image/image.lock.json').read_text())
assert build.recipe_digest() == lock['recipe_digest']
assert receipt['image'] == ci_differential.json.loads(ci_differential.RECEIPT.read_text())['image']
result = {'checked_public_files': checked, 'commit_verification': commit['verification'],
          'detached_signature_files': signature_files, 'source': receipt['source'],
          'receipt_only_descendant': True, 'reached': len(keys), 'traced': len(receipt['steps']),
          'exec_instances': sum(s['instances'] for s in receipt['steps']),
          'all_step_exit_zero': all(s['exit_status']==0 for s in receipt['steps']),
          'reported_findings': sum(len(s['findings']) for s in receipt['steps']),
          'transforms': transforms, 'commands': receipt['commands'],
          'inventory_inputs_checked': len(input_checks), 'unchanged_tools': len(inventory['tools']),
          'unchanged_residue': len(inventory['residue']),
          'inline_programs': len(names['inline_programs']), 'generated_programs': len(names['generated_programs']),
          'recipe_digest': lock['recipe_digest'], 'final_author_checks': final,
          'limit': 'Public hashes verified; no detached signature or signed commit, image archive, or raw population logs verified.'}
(PACKET/'evidence-verification.json').write_text(json.dumps(result, indent=2)+'\n')
print('PASS: public hashes, census binding, reached population, source identity, recipe, inventory inputs and final author checks')
