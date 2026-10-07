#!/usr/bin/env python3
"""Read public Git objects and source identities without using reviewer reports."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, default=Path.cwd())
p.add_argument('--sim', required=True)
a = p.parse_args()
root = a.repo.resolve()
packet = Path(__file__).resolve().parents[1]
out = packet / 'receipts'
rev = '65b9e8ee8f9e00cc303b3c294d243a89781807e9'
head = '2525eae9567865a8bc741901914bdf5a1caf2c26'
prefix = 'review-evidence/645-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
def blob(path, commit=rev):
    return git('show', commit + ':' + prefix + path)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def write(name, value):
    (out / name).write_text(json.dumps(value, indent=2) + '\n')

verified = []
for commit, selected in [('6efdd2447c72b9b60f5d0d9e393c851bb742945a', 'author/'),
                         (rev, 'author-r2d/')]:
    manifest = json.loads(blob('MANIFEST.json', commit))
    entries = [row for row in manifest if row['file'].startswith(selected)]
    for row in entries:
        assert digest(blob(row['file'], commit)) == row['published_sha256'], row['file']
    verified.append({'commit': commit, 'prefix': selected, 'verified_files': len(entries),
                     'result': 'PASS'})

r2d = 'author-r2d/round2d/'
area = json.loads(blob(r2d + 'area-ooc/comparison.json'))
rows = {}
for name in ['cmc_base', 'cmc_head', 'settle_base', 'settle_head']:
    report = blob(r2d + f'area-ooc/util_{name}.rpt').decode()
    rows[name] = {'LUT': int(re.search(r'\| Slice LUTs\*?\s*\|\s*(\d+)', report)[1]),
                  'FF': int(re.search(r'\| Slice Registers\s*\|\s*(\d+)', report)[1])}
deltas = {k: rows['cmc_head'][k] - rows['cmc_base'][k]
          + rows['settle_head'][k] - rows['settle_base'][k] for k in ['LUT', 'FF']}
assert deltas == {'LUT': 113, 'FF': 78}
assert digest((root / 'hdl/ieee1722/aaf/KL_chan_map_capture.sv').read_bytes()) == area['source_sha256']['cmc_head.sv']
quiet = json.loads(blob(r2d + 'campaigns/quiet-distributions.json'))
samples = sum(g['samples'] for g in quiet['groups'].values())
assert samples == 320462699
assert len(quiet['groups']) == 8 and all(g['phases'] == 16 for g in quiet['groups'].values())
assert all(g['min'] == -1 and g['max'] == 1 for g in quiet['groups'].values())
compare = json.loads(blob(r2d + 'campaigns/campaign-compare.json'))
assert len(compare['campaign']) == 128 and len(compare['pullin']) == 32
for group in ['campaign', 'pullin']:
    assert all(r['byte_identical'] and r['rc_round2d'] == r['rc_round2c'] == '0'
               for r in compare[group].values())
write('public-evidence-audit.json', {
    'publication_manifest_checks': verified,
    'area_rows': rows, 'computed_delta': deltas, 'limit_each': 120,
    'capture_source_hash_matches_measurement': True,
    'conservative_prior_area': {'LUT': 119, 'FF': 82},
    'quiet_samples_recounted': samples, 'quiet_peak_axis_cycles': 1,
    'quiet_groups': 8, 'phases': 128, 'windows': 512,
    'published_campaign_comparison': compare['summary'],
    'limitation': 'Campaign equality is the published comparison receipt; all individual campaign logs were not republished in this round. No independent rerun of those campaigns or implementation is claimed.'})

merges = []
for commit in ['701b8332b6bd2387471db6d55be55449e770291b', head]:
    parents = git('rev-list', '--parents', '-n', '1', commit).decode().split()[1:]
    merged = git('merge-tree', '--write-tree', *parents).decode().splitlines()[0]
    tree = git('rev-parse', commit + '^{tree}').decode().strip()
    assert merged == tree
    paths = git('diff', '--name-only', parents[0], commit).decode().splitlines()
    assert not any(x.startswith(('hdl/', 'syn/', 'constraints/', 'configs/', 'sw/litex/')) for x in paths)
    merges.append({'commit': commit, 'parents': parents, 'tree': tree,
                   'automatic_merge_equal': True, 'changed_paths': paths})
write('merge-audit.json', merges)
version = subprocess.check_output([a.sim, '--version']).decode().strip()
assert '5.050' in version
write('simulator-identity.json', {'version': version, 'launcher_sha256': digest(Path(a.sim).read_bytes())})
for path in ['campaigns/campaign-compare.json', 'campaigns/quiet-distributions.json',
             'area-ooc/comparison.json', 'functional/results.json']:
    target = out / 'public' / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob(r2d + path))
print('PASS public manifests, area arithmetic/source hash, quiet totals and published campaign comparison; two automatic merge trees')
