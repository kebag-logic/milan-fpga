#!/usr/bin/env python3
"""Reproduce exact composition checks without modifying the candidate."""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd()
PACKET = Path(__file__).resolve().parent
HEAD = 'af5be4710c3516cc247c353213d6939fa8d23f57'
PARENT = '72d3780d23a0b96362f8ae64059311b866ff5776'
SOURCE = '04e1435a218908d2b12b4053e5dab2c2dcac2ebf'
BASE = '6714181d0c8a16e2983f85b724f4d688f5111835'
TREE = 'c2aaa434de409dd97074d71567c2df41d38af65e'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.commitGraph=false', *args], env=ENV)

def changed(a, b):
    return set(git('diff', '--no-renames', '--name-only', '-z', a, b).decode().strip('\0').split('\0')) - {''}

def entries(ref):
    out = {}
    for row in git('ls-tree', '-rz', ref).split(b'\0'):
        if row:
            entry, path = row.split(b'\t', 1)
            out[path.decode()] = entry.decode()
    return out

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
assert git('show', '-s', '--format=%P', HEAD).decode().strip() == PARENT + ' ' + SOURCE
source_paths, pred_paths = changed(BASE, SOURCE), changed(BASE, PARENT)
assert changed(PARENT, HEAD) == source_paths
overlap = sorted(source_paths & pred_paths)
assert overlap == ['docs/testing/CI_WORKFLOWS.md'], overlap
print('Exact head, tree, ordered parents: PASS')
print('PR changes:', len(source_paths), 'Additional predecessor changes:', len(pred_paths))
print('Additional-predecessor overlap:', json.dumps(overlap))
for path in overlap:
    print(git('log', '--format=%h %s', BASE + '..' + PARENT, '--', path).decode())
src, pre, head = entries(SOURCE), entries(PARENT), entries(HEAD)
for path in sorted(source_paths):
    if path not in overlap:
        assert head[path] == src[path], path
    print('PR path', path, 'candidate:', head[path], 'source:', src[path])
for path in sorted(set(pre) | set(head)):
    if path not in source_paths:
        assert pre.get(path) == head.get(path), path
print('All 14 non-overlap PR entries identical to source; all paths outside PR delta identical to predecessor: PASS')
for path in sorted(pred_paths - set(overlap)):
    assert head.get(path) == pre.get(path), path
    print('Retained predecessor path:', path)

# Historical FT overlap was already in the reviewed source base.
ft = '6ca834a78'
ft_parent = git('rev-parse', '6714181d^1').decode().strip()
ft_overlap = sorted(source_paths & changed(ft_parent, BASE))
print('Historical FT overlap (already inherited by source base):', json.dumps(ft_overlap))
for path in ft_overlap:
    if path not in overlap:
        assert entries(BASE).get(path) == pre.get(path), path
print('Historical FT inputs on every shared PR path except the known #673 document overlap equal source base before #679: PASS')

# Reproduce the sole common-file merge with raw bytes, no external drivers.
path = overlap[0]
scratch = PACKET / 'scratch' / 'composition'
scratch.mkdir(parents=True, exist_ok=True)
inputs = []
for name, rev in [('source', SOURCE), ('base', BASE), ('predecessor', PARENT)]:
    f = scratch / (name + '.md')
    f.write_bytes(git('show', rev + ':' + path))
    inputs.append(str(f))
merged = subprocess.run(['git', 'merge-file', '--stdout', *inputs], capture_output=True)
assert merged.returncode == 0, merged.stderr
assert merged.stdout == (ROOT / path).read_bytes()
print('Raw three-way merge of sole overlap equals candidate bytes: PASS')

docs = (ROOT / path).read_text()
runner = (ROOT / 'scripts/run_all_suites.sh').read_text()
function = re.search(r'^suite_timeout\(\) \{.*?^\}', runner, re.M | re.S).group()
budgets = {'capture_coherence':2400, 'milan_dp_mclk':3600, 'milan_dp':4800, 'milan_dp_gptp':5400, 'mmcm_servo':1800, 'aaf':1800}
for suite, expected in budgets.items():
    env = dict(ENV)
    env.pop('SUITE_TIMEOUT', None)
    got = subprocess.check_output(['bash', '-c', function + '\nsuite_timeout "$1"', 'probe', suite], env=env).decode().strip()
    assert int(got) == expected, (suite, got)
    label = 'every other default suite' if suite == 'aaf' else '`' + suite + '`'
    assert re.search(r'^\| ' + re.escape(label) + r'[^|]*\| ' + str(expected) + r' s \|', docs, re.M), suite
    env['SUITE_TIMEOUT'] = '71'
    got = subprocess.check_output(['bash', '-c', function + '\nsuite_timeout "$1"', 'probe', suite], env=env).decode().strip()
    assert got == '71'
    print('Deadline/document/explicit override:', suite, expected, 'PASS')

import yaml
workflow = yaml.safe_load((ROOT / '.github/workflows/rtl-fast.yml').read_text())
job = workflow['jobs']['firmware-unit']
steps = job['steps']
install = next(i for i,s in enumerate(steps) if 'ci_rv32_sdk.py --destination' in s.get('run',''))
for script in ['fw_rv32_selftest.py', 'test_ctrl_firmware.py', 'test_ctrl_nvm.py']:
    found = [(i,s) for i,s in enumerate(steps) if script in s.get('run','')]
    assert len(found) == 1 and found[0][0] > install
    assert script + ' --require-rv32' in found[0][1]['run']
    assert 'if' not in found[0][1] and not found[0][1].get('continue-on-error')
    print('Required RV32 step after SDK:', script, 'PASS')
assert 'firmware-unit' in workflow['jobs']['rtl-fast']['needs']
sys.path.insert(0, str(ROOT / 'scripts'))
import ci_scope
for path in sorted(source_paths - {'docs/testing/CI_WORKFLOWS.md'}):
    assert not ci_scope.is_doc_only_path(path), path
print('All firmware and workflow PR paths select relevant CI: PASS')
print('Composition probe: PASS')
