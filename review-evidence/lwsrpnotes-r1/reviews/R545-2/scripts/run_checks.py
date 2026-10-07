#!/usr/bin/env python3
"""Reproduce the focused review; all child commands are waited for directly."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

PACKET = Path(__file__).resolve().parents[1]
SCRATCH = PACKET / 'scratch'
RECEIPTS = PACKET / 'receipts'
HEAD = 'f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152'

def run(label, command, cwd, env=None, timeout=540):
    started = time.monotonic()
    with (RECEIPTS / (label + '.log')).open('w') as log:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=timeout)
    rc = result.returncode
    (RECEIPTS / (label + '.rc')).write_text(str(rc) + '\n')
    (RECEIPTS / (label + '.json')).write_text(json.dumps({
        'command': command, 'cwd': str(cwd), 'rc': rc,
        'elapsed_seconds': round(time.monotonic() - started, 3),
        'head': HEAD,
    }, indent=2) + '\n')
    print(f'{label}: rc={rc}', flush=True)
    return rc

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', choices=['dependency', 'docs', 'links', 'graphs', 'OFF', 'ON'])
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip() == HEAD
    SCRATCH.mkdir(exist_ok=True)
    RECEIPTS.mkdir(exist_ok=True)
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['TMPDIR'] = str(SCRATCH)
    prefix = SCRATCH / 'unit-prefix'
    env['LD_LIBRARY_PATH'] = str(prefix / 'lib') + os.pathsep + env.get('LD_LIBRARY_PATH', '')
    failures = 0
    if args.task == 'dependency':
        source = SCRATCH / 'cgreen-source'
        build = SCRATCH / 'cgreen-build'
        commands = [
            ('dependency-fetch', ['git', 'clone', '--depth', '1', '--branch', '1.7.0',
                                  'https://github.com/cgreen-devs/cgreen.git', str(source)]),
            ('dependency-configure', ['cmake', '-S', str(source), '-B', str(build),
                                     '-DCMAKE_BUILD_TYPE=Release', f'-DCMAKE_INSTALL_PREFIX={prefix}',
                                     '-DCGREEN_WITH_TESTS=OFF', '-DCGREEN_WITH_EXAMPLES=OFF']),
            ('dependency-build', ['make', '-C', str(build), '-j16']),
            ('dependency-install', ['cmake', '--install', str(build)]),
        ]
        for label, command in commands:
            if run(label, command, repo, env):
                return 1
            if label == 'dependency-fetch':
                resolved = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
                assert resolved == 'feeb85ed48d163f6b7b0011a6d8e6043951541e4'
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True)
        (RECEIPTS / 'dependency-commit.txt').write_text(sha)
    elif args.task == 'docs':
        for label, command in [
            ('sentences', ['python3', 'doc/tools/check_sentences.py']),
            ('references', ['python3', 'doc/tools/check_references.py']),
            ('references-self-test', ['python3', 'doc/tools/check_references.py', '--self-test']),
            ('whitespace', ['git', 'diff', '--check', 'a4cbe41de1c80d43f26e0d348cbdb45075273a4f', HEAD]),
        ]:
            failures += bool(run(label, command, repo, env))
    elif args.task == 'links':
        failures += bool(run('links', ['python3', 'doc/tools/check_links.py', '--github-auth'], repo, env))
    elif args.task == 'graphs':
        failures += bool(run('graphs', ['python3', 'doc/tools/render_mermaid.py', '--output',
                                       str(SCRATCH / 'graphs')], repo, env))
    else:
        profile = args.task
        build = SCRATCH / ('unit-' + profile)
        commands = [
            ('configure', ['cmake', '-S', str(repo), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug',
                           f'-DCMAKE_PREFIX_PATH={prefix}', f'-DLWSRP_MILAN={profile}']),
            ('build', ['make', '-C', str(build), '-j16']),
            ('ctest', ['ctest', '--test-dir', str(build), '--output-on-failure']),
            ('unit', [str(build / 'unit_tests')]),
        ]
        for label, command in commands:
            # Keep the aggregate compiler count at 16 across profile processes.
            with (SCRATCH / 'build.lock').open('w') as lock:
                if label == 'build':
                    fcntl.flock(lock, fcntl.LOCK_EX)
                rc = run(profile + '-' + label, command, repo, env)
            if rc:
                return 1
    return int(bool(failures))

if __name__ == '__main__':
    sys.exit(main())
