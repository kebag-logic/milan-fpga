# SPDX-License-Identifier: Apache-2.0
"""Reproduce graph rendering and the isolated published codec command."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--jobs', type=int, default=2)
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
scratch = packet / 'scratch'
prefix = scratch / 'cgreen'
config = scratch / 'browser.json'
config.write_text(json.dumps({'args': ['--no-sandbox']}))
env = os.environ | {'PYTHONDONTWRITEBYTECODE': '1', 'LD_LIBRARY_PATH': str(prefix / 'lib'), 'CPATH': str(prefix / 'include'), 'LIBRARY_PATH': str(prefix / 'lib'), 'TMPDIR': str(scratch)}
def run(label, command, stdin=None):
    r = subprocess.run(list(map(str, command)), cwd=source, env=env, input=stdin, capture_output=True, text=True, timeout=540)
    output = (r.stdout + r.stderr).replace(str(source), '$SOURCE').replace(str(packet), '$PACKET')
    (packet / 'receipts' / (label + '.log')).write_text(output)
    (packet / 'receipts' / (label + '.rc')).write_text(str(r.returncode) + '\n')
    print(label, r.returncode, output[-300:], flush=True)
    return r.returncode
def codec():
    binary = scratch / 'codec'
    code = '#include <cgreen/cgreen.h>\nTestSuite *mrp_pdu_suite(void);\nint main(void) { return run_test_suite(mrp_pdu_suite(), create_text_reporter()); }\n'
    result = run('codec-build', ['cc', '-std=c11', '-Isrc/include', 'tests/unit/mrp_pdu_test.c', 'src/core/mrp_pdu.c', '-xc', '-', '-lcgreen', '-o', binary], code)
    return result or run('codec', [binary])
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs, 2)) as pool:
    jobs = [pool.submit(codec), pool.submit(run, 'docs-graphs', ['python3', 'doc/tools/render_mermaid.py', '--output', scratch / 'graphs', '--puppeteer-config', config])]
    results = [job.result() for job in jobs]
raise SystemExit(any(results))
