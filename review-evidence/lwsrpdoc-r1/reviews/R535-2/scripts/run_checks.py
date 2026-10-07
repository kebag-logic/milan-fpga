#!/usr/bin/env python3
"""Run independent documentation and host checks, keeping scratch outside source."""
import argparse
import concurrent.futures
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('packet', type=Path)
args = parser.parse_args()
source, packet = args.source.resolve(), args.packet.resolve()
scratch = packet / 'scratch'
receipts = packet / 'receipts'
scratch.mkdir(exist_ok=True)
receipts.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
(scratch / 'temporary').mkdir(exist_ok=True)
env['TMPDIR'] = str(scratch / 'temporary')
(scratch / 'browser.json').write_text(json.dumps({'args':['--no-sandbox'], 'userDataDir':str(scratch/'render-profile')})+'\n')
sdk = scratch / 'sdk'
for key, value in [('CMAKE_PREFIX_PATH', sdk), ('CPATH', sdk / 'include'),
                   ('LIBRARY_PATH', sdk / 'lib'), ('LD_LIBRARY_PATH', sdk / 'lib')]:
    env[key] = str(value) + (os.pathsep + env[key] if env.get(key) else '')

def run(name, command, cwd=source, expected=0):
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=540)
    # Portable paths in otherwise unchanged command output.
    output = result.stdout.replace(str(packet), '$PACKET').replace(str(source), '$SOURCE')
    (receipts / (name + '.log')).write_text(output)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(f'{name}: rc={result.returncode}, expected={expected}', flush=True)
    if result.returncode != expected:
        print(output[-2500:], flush=True)
    return result.returncode

archive = subprocess.check_output(['git', 'archive', 'HEAD'], cwd=source)
host = scratch / 'host'
host.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(host, filter='data')

def host_checks():
    if run('host-configure', ['cmake', '-S', '.', '-B', 'build', '-DCMAKE_BUILD_TYPE=Debug'], host):
        return
    if run('host-build', ['cmake', '--build', 'build', '--parallel', '2'], host):
        return
    # These independent executions only read the completed build.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(run, name, command, host) for name, command in [
            ('ctest', ['ctest', '--test-dir', 'build', '--output-on-failure']),
            ('unit-direct', ['./build/unit_tests']),
            ('scenarios', ['behave']),
            ('scenario-dry-run', ['behave', '--dry-run']),
        ]]
        for job in jobs:
            job.result()
    codec_command = """cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests <<'C'
#include <cgreen/cgreen.h>
TestSuite *mrp_pdu_suite(void);
int main(void)
{
    return run_test_suite(mrp_pdu_suite(), create_text_reporter());
}
C
"""
    if run('codec-compile', ['bash', '-c', codec_command], host) == 0:
        run('codec-run', ['./build/mrp_pdu_tests'], host)

def reference_mutations():
    probe = scratch / 'reference-probe'
    probe.mkdir(exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(probe, filter='data')
    page = probe / 'README.md'
    original = page.read_bytes()
    for name, text in [('bare-c11', 'C11'), ('inline-c11', '`C11`'), ('bare-iso', 'ISO/IEC 9899:2011'), ('bare-spdx', 'SPDX')]:
        page.write_bytes(original + f'\nUse {text}.\n'.encode())
        run(name, ['python3', 'doc/tools/check_references.py'], probe, expected=1)
    page.write_bytes(original)
    run('reference-restored', ['python3', 'doc/tools/check_references.py'], probe)

commands = [
    ('sentences', ['python3', 'doc/tools/check_sentences.py'], 0),
    ('references', ['python3', 'doc/tools/check_references.py'], 0),
    ('reference-self-test', ['python3', 'doc/tools/check_references.py', '--self-test'], 0),
    ('links', ['python3', 'doc/tools/check_links.py', '--github-auth'], 1),
    ('graph-render', ['python3', 'doc/tools/render_mermaid.py', '--output', str(packet / 'graphs'),
                      '--puppeteer-config', str(scratch / 'browser.json')], 0),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
    futures = [pool.submit(run, name, command, source, expected) for name, command, expected in commands]
    futures += [pool.submit(host_checks), pool.submit(reference_mutations)]
    for future in futures:
        future.result()
print('All foreground campaigns completed.', flush=True)
