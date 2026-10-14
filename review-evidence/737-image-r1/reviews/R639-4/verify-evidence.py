#!/usr/bin/env python3
"""Compare public execution receipts and source-bound group coverage."""
import ast
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
p = packet / 'scratch/public'
digest = lambda data: hashlib.sha256(data).hexdigest()
read = lambda name: json.loads((p / name).read_text())
lock = json.loads((root / 'ci/image/image.lock.json').read_text())
source = root / 'sw/builder/test_builder.py'
source_hash = digest(source.read_bytes())
tree = ast.parse(source.read_text())
main = next(n for n in tree.body if isinstance(n, ast.If) and ast.unparse(n.test) == "__name__ == '__main__'")
loop = next(n for n in main.body if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == 'fn')
expected = [n.id for n in loop.iter.elts]
returned = []
for i in range(9):
    group = read(f'builder-functions-{i}.json')
    assert group['source_sha256'] == source_hash and group['require_rv32']
    names = [r['name'] for r in group['results']]
    assert names == group['groups'][i]
    returned.extend(names)
    receipt = read('builder-home-background.receipt.json' if i == 1 else f'builder-group-{i}-0.receipt.json')
    assert receipt['rc'] == 0 and '--require-rv32' in receipt['command']
assert collections.Counter(expected) == collections.Counter(returned)
assert len(returned) == len(set(returned)) == 103
verified = []
for name in ('round4-final-gates.json', 'round4-markdown-final.json', 'round4-rebuilt-image.json',
             'round4-lock.json', 'round4-second-archive.json'):
    for row in read(name):
        assert row['rc'] == 0
        data = (p / row['log']).read_bytes()
        assert len(data) == row['size'] and digest(data) == row['sha256']
        verified.append(dict(receipt=name, gate=row['gate'], log=row['log'], sha256=digest(data), rc=0))
for which in ('a','b'):
    recipe = read(f'round4-cold-lock-{which}-recipe.json')
    assert all(digest((root / name).read_bytes()) == value for name,value in recipe['inputs'].items())
    assert recipe['sha256'] == lock['recipe_digest']
    record = read(f'round4-cold-lock-{which}-validation-tools.receipt.json')
    assert record['image_digest'] == lock['image_digest'] and record['image_id'] == lock['image_id']
    metadata = read(f'round4-cold-lock-{which}-validation-tools.metadata.json')
    args = metadata['buildx.build.provenance']['invocation']['parameters']['args']
    assert 'no-cache' in args and args['force-network-mode'] == 'none'
old = json.loads(subprocess.check_output(['git','show','e6b86814:ci/image/tool-inventory.json'],cwd=root))
current = json.loads((root / 'ci/image/tool-inventory.json').read_text())
assert old['tools'] == current['tools']
old_lock = json.loads(subprocess.check_output(['git','show','18f2df92:ci/image/image.lock.json'],cwd=root))
unchanged_layers = [a['tool'] for a,b in zip(lock['layers'],old_lock['layers'])
                    if (a['oci_digest'],a['diff_id']) == (b['oci_digest'],b['diff_id'])]
smoke = (p / 'round4-rebuilt-image-smoke.log').read_text()
assert 'PASS: all image tool families' in smoke and 'GNU Make 4.3' in smoke and '3.12.3' in smoke
hosted = (packet / 'scratch/hosted-docs.log').read_text()
skip = next(line for line in hosted.splitlines() if 'SKIP: the MAKEFLAGS += -e mutation' in line)
runner = (packet / 'scratch/runner-readme.md').read_text()
make = next(line for line in runner.splitlines() if '| make ' in line)
assert '4.3-4.1build2' in make
pins = json.loads((root / 'ci/image/sources.lock.json').read_text())
assert next(r['version'] for r in pins['packages'] if r['tool'] == 'make') == '4.3-4.1build2'
result = dict(source_hash=source_hash, builder_invocations=len(returned), builder_groups=9,
              exact_cover=True, historical_builder_head='18f2df92b13cb3f4036b073ed76940187bf10487',
              manager_source_bank=False, verified_logs=verified, cold_metadata_no_cache=True,
              recipe_inputs_equal_head=True, unchanged_round2_tool_layers=unchanged_layers,
              tool_records_unchanged_from_round3=len(current['tools']),
              hosted_job='https://github.com/kebag-logic/milan-fpga/actions/runs/38584726767/job/115923539474',
              hosted_head='113493920448a8fe6cebd7988408f071b99894c8',
              hosted_skip_excerpt=skip, runner_make_row=make, make_versions_equal=True)
(packet / 'evidence-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:', len(verified), 'public gate logs; exact 103-invocation cover; matching cold recipes; hosted skip/version parity')
