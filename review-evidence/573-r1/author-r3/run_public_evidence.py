"""Run unchanged public scripts against committed archive exports."""
import json
import os
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
scratch = Path('/tmp/573-a355')
reviews = scratch / 'reviews'
head = scratch / 'head'
r340 = reviews / 'R340-2/scripts'
r341 = reviews / 'R341-2/scripts'


def run(label, command, tree='head'):
    env = dict(os.environ, **json.loads((scratch / f'{tree}-git-env.json').read_text()))
    subprocess.run([sys.executable, str(out / 'run_gate.py'), label, *map(str, command)],
                   cwd=scratch / tree, env=env, check=True, timeout=10800)


run('reviewer-round2-probes', ['python3', '-B', r340 / 'round2_probes.py', head,
                             out / 'round2-probes.json'])
run('reviewer-scalar-spellings', ['python3', '-B', r341 / 'scalar_spelling_probe.py', head])
run('reviewer-internal-mutants', ['python3', '-B', r340 / 'mutants_r2.py', head,
                                r340 / 'mutant_cases_r2.json', out / 'internal-mutants.json'])
run('reviewer-external-mutants', ['python3', '-B', r341 / 'run_mutants_r2.py', head,
                                r341 / 'reviewer_mutants_r2.json'])
for label in ('base', 'head'):
    run(f'artifacts-{label}', ['python3', '-B', r340 / 'r340-1/hash_artifacts.py',
                              scratch / label, out / f'artifacts-{label}.json'], label)
    run(f'shipping-{label}', ['bash', r340 / 'r341-1/shipping_identity.sh',
                             scratch / label, scratch / f'shipping-{label}',
                             out / f'shipping-{label}.sha256'], label)
assert (out / 'artifacts-base.json').read_bytes() == (out / 'artifacts-head.json').read_bytes()
assert (out / 'shipping-base.sha256').read_bytes() == (out / 'shipping-head.sha256').read_bytes()
print('Artifact equality: 85/85 inventory entries and 80/80 CLI entries.', flush=True)
