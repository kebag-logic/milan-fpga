#!/usr/bin/env python3
"""Record each command, stdout, stderr and exit; assert contract outcomes."""
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
work = Path((OUT / 'work-directory.txt').read_text().strip())
receipts = OUT / 'receipts' / 'focused'
receipts.mkdir(exist_ok=True)
base_env = dict(os.environ, PYTHONUTF8='0', PYTHONCOERCECLOCALE='0',
                PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_NOSYSTEM='1',
                GIT_CONFIG_GLOBAL='/dev/null', GIT_TERMINAL_PROMPT='0',
                OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MAKEFLAGS='-j1')
environments = {
    'utf8': dict(base_env, LC_ALL='C.UTF-8'),
    'latin1': dict(base_env, LC_ALL='en_US.ISO-8859-1', LOCPATH=str(work / 'lp' / 'locale')),
}


def run(label, args, env, cwd):
    command = ['rtk', 'proxy', *map(str, args)]
    result = subprocess.run(command, env=env, cwd=cwd, capture_output=True)
    (receipts / (label + '.stdout')).write_bytes(result.stdout)
    (receipts / (label + '.stderr')).write_bytes(result.stderr)
    (receipts / (label + '.json')).write_text(json.dumps({
        'argv': command, 'cwd': str(cwd), 'returncode': result.returncode,
        'environment_overrides': {key: env[key] for key in base_env
                                  if base_env.get(key) != os.environ.get(key)},
        'LC_ALL': env['LC_ALL'], 'LOCPATH': env.get('LOCPATH'), 'jobs': 1,
    }, indent=2) + '\n')
    return result


results = []
for locale, env in environments.items():
    for version in ('head', 'base'):
        source = work / 'lp' / version
        label = f'sites-{version}-{locale}'
        proc = run(label, ['python3', '-B', OUT / 'filename_checks.py', source,
                           work, 'sites', receipts / (label + '.gitcalls.jsonl')],
                   env, work)
        print(label, 'exit', proc.returncode)
        if proc.returncode:
            raise SystemExit('site observation failed')
        for fixture in ('linear', 'merge'):
            label = f'cli-{fixture}-{version}-{locale}'
            proc = run(label, ['python3', '-B', source / 'scripts/check_merge_containment.py',
                               '--no-fetch', '--base', 'main', 'pr'],
                       env, work / 'lp' / fixture)
            token = proc.stdout.split()[0].decode('ascii') if proc.stdout.split() else 'NO_OUTPUT'
            expected = 'UNKNOWN' if fixture == 'merge' and version == 'head' else 'STRANDED'
            passed = proc.returncode == 1 and token == expected
            results.append({'case': label, 'expected': [1, expected],
                            'measured': [proc.returncode, token], 'pass': passed})
            print(label, 'expected', (1, expected), 'measured', (proc.returncode, token),
                  'PASS' if passed else 'FAIL')
    label = f'existing-path-format-head-{locale}'
    proc = run(label, ['python3', '-B', OUT / 'filename_checks.py', work / 'lp/head',
                       work, 'existing-path-format', receipts / (label + '.gitcalls.jsonl')],
               env, work)
    print(label, 'exit', proc.returncode,
          proc.stdout.decode('ascii', 'backslashreplace').splitlines()[-1:])
    if proc.returncode:
        raise SystemExit('existing focused controls failed')

(receipts / 'regression-assertions.json').write_text(json.dumps(results, indent=2) + '\n')
failed = sum(not row['pass'] for row in results)
print(f'Contract assertions: {len(results)} total, {failed} failed.')
raise SystemExit(bool(failed))
