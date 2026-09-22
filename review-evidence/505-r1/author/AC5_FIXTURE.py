#!/usr/bin/env python3
"""Generate AC5 execution copies INSIDE a disposable uncredentialed CI job.

This is experiment data generation, not host orchestration. Never import or
execute this file on the host. The manager supplies the exact candidate SHA.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess

import yaml


INJECTION = r'''
import os
from pathlib import Path
import subprocess

assert Path('/.dockerenv').is_file(), 'CI job container required'
assert not Path('/var/run/docker.sock').exists(), 'no Docker socket in job'
assert not any(os.environ.get(k) for k in
               ('GH_TOKEN', 'GITHUB_TOKEN', 'DOCKER_HOST', 'SSH_AUTH_SOCK'))
mode = @MODE@
kind = @KIND@
expected_sha = @SHA@
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == expected_sha, (head, expected_sha)
subprocess.run(['python3', 'scripts/ci_events.py', '--check'], check=True)
print('AC5_BASELINE_CONTRACT=PASS', flush=True)

if mode == 'swallow':
    path = Path('.github/workflows/docs.yml')
    source = path.read_text()
    old = '          python3 scripts/check_py_idiom.py\n'
    assert source.count(old) == 1
    path.write_text(source.replace(old, old.rstrip('\n') + ' || true\n'))
    print('AC5_MUTATION=Python idiom gate line 1 appends || true', flush=True)

if kind == 'docs' and mode != 'clean':
    path = Path('scripts/ci_scope.py')
    source = path.read_text()
    assert '_carrier_script_407_probe' not in source
    path.write_text(source + '\n\ndef _carrier_script_407_probe() -> None:\n'
                    '    """AC5 finding planted only in a disposable job."""\n'
                    '    try:\n'
                    '        pass\n'
                    '    except:\n'
                    '        pass\n')
    run = subprocess.run(['python3', 'scripts/check_py_idiom.py'],
                         capture_output=True, text=True)
    print(run.stdout, end='', flush=True)
    print(run.stderr, end='', flush=True)
    assert run.returncode == 1, run.returncode
    assert 'bare except: 1' in run.stdout, run.stdout
    print('AC5_UNMASKED_IDIOM_RC=1 (bare except)', flush=True)
print('AC5_INJECTION_COMPLETE', flush=True)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sha', required=True)
    parser.add_argument('--mode', choices=('clean', 'defect', 'swallow'), required=True)
    args = parser.parse_args()
    assert Path('/.dockerenv').is_file(), 'generate only inside a CI container'
    assert not Path('/var/run/docker.sock').exists(), 'no Docker socket in job'
    assert not any(os.environ.get(k) for k in
                   ('GH_TOKEN', 'GITHUB_TOKEN', 'DOCKER_HOST', 'SSH_AUTH_SOCK'))
    head = subprocess.check_output(['git', '-C', str(args.root), 'rev-parse', 'HEAD'],
                                   text=True).strip()
    assert head == args.sha, (head, args.sha)
    args.output.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for kind, workflow in (('docs', 'docs.yml'), ('rtl', 'rtl.yml')):
        path = args.root / '.github/workflows' / workflow
        source = path.read_bytes()
        hashes[workflow] = hashlib.sha256(source).hexdigest()
        original = yaml.safe_load(source)
        fixture = copy.deepcopy(original)
        # PyYAML's YAML 1.1 reader treats the Actions key `on` as True.
        if True in fixture:
            fixture['on'] = fixture.pop(True)
        fixture['name'] = f'carrier-script-407-{kind}-{args.mode}'
        jid = 'docs-check' if kind == 'docs' else 'full-ci-gate'
        target = ('Python idiom gate' if kind == 'docs'
                  else 'Hold every workflow file to its contract')
        steps = fixture['jobs'][jid]['steps']
        at = next(n for n, step in enumerate(steps) if step.get('name') == target)
        if kind == 'docs' and args.mode == 'swallow':
            old = 'python3 scripts/check_py_idiom.py\n'
            assert steps[at]['run'].count(old) == 1
            steps[at]['run'] = steps[at]['run'].replace(old, old.rstrip('\n') + ' || true\n')
        injection = (INJECTION.replace('@MODE@', repr(args.mode))
                     .replace('@KIND@', repr(kind)).replace('@SHA@', repr(args.sha)))
        steps.insert(at, {
            'name': 'AC5 disposable injection and unmasked control',
            'run': 'python3 -m pip install --quiet pyyaml\n'
                   + "python3 - <<'PY'\n" + injection + '\nPY\n',
        })
        # No production job, dependency, guard, or original step is dropped.
        assert set(fixture['jobs']) == set(original['jobs'])
        for job_id, job in original['jobs'].items():
            assert {k: v for k, v in job.items() if k != 'steps'} == {
                k: v for k, v in fixture['jobs'][job_id].items() if k != 'steps'}
        out = args.output / f'carrier-script-407-{kind}-{args.mode}.yml'
        out.write_text(yaml.safe_dump(fixture, sort_keys=False, width=1000))
        print(out)
    (args.output / f'inputs-{args.mode}.json').write_text(json.dumps({
        'candidate_sha': args.sha, 'source_workflow_sha256': hashes,
        'mode': args.mode, 'status': 'generated only; real act execution required',
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
