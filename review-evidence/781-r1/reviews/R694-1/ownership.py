#!/usr/bin/env python3
"""Check every serial and CI unit against independently collected shard lists."""
from collections import Counter
from pathlib import Path
import json
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent / 'ownership'
out.mkdir(exist_ok=True)
def listing(name, *args):
    r = subprocess.run(['bash', 'scripts/run_all_suites.sh', *args, '--list'],
                       cwd=root, text=True, capture_output=True, check=True)
    (out / (name+'.txt')).write_text(r.stdout)
    assert not r.stderr, r.stderr
    return r.stdout.splitlines()
serial = listing('serial')
pieces = listing('pieces', '--ci-pieces')
owned = [listing(f'shard-{k}', '--ci-pieces', '--shard', f'{k}/17') for k in range(17)]
assert len(serial) == 64 and len(set(serial)) == 64
assert len(pieces) == 81 and len(set(pieces)) == 81
assert Counter(x for group in owned for x in group) == Counter(pieces)
assert 'media_phase' in owned[4]
assert owned[16] == ['milan_dp_mclk__0']
assert 'tsn_fuzz' in owned[1] and 'chmap_capture' in owned[3]
sys.path.insert(0, str(root/'scripts'))
import suite_shards as s
owners, load = s.balance(pieces, 17)
bounds = [m*36 for m in s.verilator_worker_limits(s.WORKFLOW.read_text())]
assert all(v <= b for v,b in zip(load,bounds))
for k,group in enumerate(owned):
    assert all(owners[x] == k for x in group)
    print(f'{k}/17: {load[k]} <= {bounds[k]} s; '+', '.join(group))
print('PASS: 64 serial suites; 81 CI units each owned exactly once; specialized owners and every bound correct')
(out/'loads.json').write_text(json.dumps(dict(load=load,bounds=bounds),indent=2)+'\n')
