#!/usr/bin/env python3
"""Create retained variants only in the two freshly created fixture repos."""
import json
import os
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
work = Path((OUT / 'work-directory.txt').read_text().strip())
receipts = OUT / 'receipts' / 'positive-controls'
receipts.mkdir(exist_ok=True)
env = dict(os.environ, LC_ALL='C.UTF-8', PYTHONUTF8='0', PYTHONCOERCECLOCALE='0',
           PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_NOSYSTEM='1',
           GIT_CONFIG_GLOBAL='/dev/null', GIT_TERMINAL_PROMPT='0',
           GIT_AUTHOR_NAME='R251 fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
           GIT_COMMITTER_NAME='R251 fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid',
           GIT_AUTHOR_DATE='@1790100000 +0000', GIT_COMMITTER_DATE='@1790100000 +0000')
records = []


def run(label, argv, cwd, environment):
    command = ['rtk', 'proxy', *map(str, argv)]
    result = subprocess.run(command, cwd=cwd, env=environment, capture_output=True)
    (receipts / (label + '.stdout')).write_bytes(result.stdout)
    (receipts / (label + '.stderr')).write_bytes(result.stderr)
    records.append({'label': label, 'argv': command, 'cwd': str(cwd),
                    'LC_ALL': environment['LC_ALL'], 'LOCPATH': environment.get('LOCPATH'),
                    'returncode': result.returncode})
    return result


checks = []
for fixture, content in [('linear', b'v1 stranded work\n'), ('merge', b'v1 source work\n')]:
    repo = work / 'lp' / fixture
    run(fixture + '-checkout', ['git', 'checkout', '-q', '-b', 'retained', 'main'], repo, env).check_returncode()
    with open(os.fsencode(repo) + b'/\xc3\xa9.txt', 'wb') as stream:
        stream.write(content)
    run(fixture + '-add', ['git', 'add', '-A'], repo, env).check_returncode()
    run(fixture + '-commit', ['git', '-c', 'commit.gpgsign=false', 'commit', '-qm',
                             'Retain exact non-ASCII source content'], repo, env).check_returncode()
    for locale in ('utf8', 'latin1'):
        environment = dict(env)
        if locale == 'latin1':
            environment.update(LC_ALL='en_US.ISO-8859-1', LOCPATH=str(work / 'lp/locale'))
        label = fixture + '-' + locale
        result = run(label, ['python3', '-B', work / 'lp/head/scripts/check_merge_containment.py',
                             '--no-fetch', '--base', 'retained', 'pr'], repo, environment)
        passed = result.returncode == 0 and result.stdout.split()[0] == b'contained'
        if fixture == 'merge':
            passed = passed and b'raw no-op retention' in result.stdout
        checks.append({'case': label, 'pass': passed, 'returncode': result.returncode})
        print(label, 'PASS' if passed else 'FAIL', result.stdout.decode('ascii', 'backslashreplace').strip())

(receipts / 'execution.json').write_text(json.dumps({
    'commands': records, 'checks': checks, 'jobs': 1,
    'environment_overrides': {key: value for key, value in env.items()
                              if os.environ.get(key) != value},
    'fixture_write': {'path_bytes_hex': b'\xc3\xa9.txt'.hex(),
                      'linear_bytes_hex': b'v1 stranded work\n'.hex(),
                      'merge_bytes_hex': b'v1 source work\n'.hex()},
}, indent=2) + '\n')
raise SystemExit(any(not check['pass'] for check in checks))
