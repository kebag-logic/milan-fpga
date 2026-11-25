#!/usr/bin/env python3
"""Reproduce bounded documentation checks without changing source files."""
import concurrent.futures
import json
import os
import pathlib
import re
import subprocess
import sys

OUT = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
HEAD = '09201d35d7ea720b3ba205da185ba35c159ec24a'
DOCHEAD = '1516b2ffe321337858389ec8e42897f8a80644bb'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_NO_REPLACE_OBJECTS='1', TMPDIR=str(OUT / 'scratch'))

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=env).decode()

assert git('rev-parse', 'HEAD').strip() == HEAD
files = git('diff', '--name-only', 'c413d33a', DOCHEAD).splitlines()
assert files == ['docs/testing/CI_WORKFLOWS.md', 'docs/testing/TESTING.md']
driver = (ROOT / 'scripts/run_all_suites.sh').read_text()
function = driver.split('suite_timeout() {', 1)[1].split('\n}', 1)[0]
arms = dict(re.findall(r'([\w*]+)\)\s+printf.*?SUITE_TIMEOUT:-(\d+)', function))
assert arms == {'capture_coherence':'2400', 'input_loopback':'300', 'input_loopback_dp':'300', 'milan_dp':'4800', 'milan_dp_gptp':'6900', 'milan_dp_mclk':'3600', 'media_phase':'1400', 'reboot_ctrl':'300', '*':'1800'}
policy = (ROOT / 'docs/testing/CI_WORKFLOWS.md').read_text()
table = policy.split('| Suite | Budget | Basis |', 1)[1].split('\n\n', 1)[0]
for suite, budget in arms.items():
    assert (suite == '*' and '| every other default suite | 1800 s |' in table) or (f'`{suite}`' in table and any(f'`{suite}`' in row and f'{budget} s' in row for row in table.splitlines()))
assert 'their hosted windows are owed' in table
expected = "Both are provisional under the new-suite steps in the selector's docstring: each figure in `scripts/suite_shards.py` is 300 s."
assert expected in (ROOT / 'docs/testing/TESTING.md').read_text()
(OUT / 'scope.txt').write_text('HEAD ' + HEAD + '\nTREE ' + git('rev-parse', 'HEAD^{tree}') + '\nOriginal documentation commit:\n' + git('diff', '--stat', 'c413d33a', DOCHEAD) + '\nRequested range to actual HEAD:\n' + git('diff', '--stat', 'c413d33a', HEAD) + '\nFirst-parent history:\n' + git('log', '--first-parent', '--format=%H %s', 'c413d33a..HEAD') + '\nDocumentation patch:\n' + git('diff', 'c413d33a', DOCHEAD))
commands = {
    'docs-hygiene': ['python3', 'scripts/docs_check.py'],
    'docs-style': ['python3', 'scripts/check_doc_style.py'],
    'docs-em-dash': ['python3', 'scripts/check_em_dash.py', '--base', 'c413d33a'],
    'whitespace': ['git', 'diff', '--check', 'c413d33a', HEAD],
}
def run(item):
    name, cmd = item
    proc = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.stdout.decode(errors='replace').replace(str(ROOT), '<checkout>').replace(str(OUT), '<packet>')
    (OUT / (name + '.log')).write_text(output)
    (OUT / (name + '.rc')).write_text(str(proc.returncode) + '\n')
    return {'name': name, 'argv': cmd, 'rc': proc.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
(OUT / 'docs-results.json').write_text(json.dumps({'head':HEAD, 'budget_arms':arms, 'budget_table_matches':True, 'wording_fix_matches':True, 'results':results}, indent=2) + '\n')
print(json.dumps(results))
