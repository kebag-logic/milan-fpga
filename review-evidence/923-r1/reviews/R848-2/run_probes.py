#!/usr/bin/env python3
"""Reproduce the delta's positive cases and three named negative controls in disposable directories."""
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
names = ('app-if1', 'app-if2', 'old-write-drop', 'stop-at-lost-reply', 'ignore-pick')
if len(sys.argv) == 2:
    def job(name):
        result = subprocess.run([sys.executable, '-B', __file__, str(repo), name], text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (packet / (name + '.log')).write_text(result.stdout)
        (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
        return {'probe': name, 'rc': result.returncode}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(job, names))
    print(json.dumps(results, indent=2))
    sys.exit(int(any(r['rc'] for r in results)))

name = sys.argv[2]
assert name in names
scratch = packet / 'scratch' / name
scratch.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(scratch)
sys.path[:0] = [str(repo / 'sw/firmware/ctrl/test'), str(repo / 'sw/firmware/gtest')]
import aecp_arms
import fw_gtest
from ctrl_build import CTRL, STACK, Tree

src = CTRL
selected = '*'
mode = 'app' if name.startswith('app-') else 'mailbox'
interfaces = 1 if name == 'app-if1' else 2
expected = []
agreement = "GET_AUDIO_MAP and the datapath's store hold the same mappings"
if name == 'old-write-drop':
    text = (aecp_arms.HERE / 'test_aecp.cpp').read_text()
    old = '        if(verdict==2u&&!reserved){*reply=MBX_MODEL_SILENT;return 0;}'
    assert text.count(old) == 1
    text = text.replace(old, '        if(verdict==2u){(void)reserved;*reply=MBX_MODEL_SILENT;return 0;}')
    testdir = scratch / 'test'
    testdir.mkdir(exist_ok=True)
    (testdir / 'test_aecp.cpp').write_text(text)
    aecp_arms.HERE = testdir
    selected = 'Face.ALostReply*:Face.AnUnansweredEditFailsUntilItsCommitIsReserved'
    expected = [(t, agreement) for t in (
        'Face.AnUnansweredEditFailsUntilItsCommitIsReserved',
        'Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing',
        'Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing')]
elif name in ('stop-at-lost-reply', 'ignore-pick'):
    src = scratch / 'ctrl'
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', 'obj*'))
    path = src / 'aecp/aecp_face.c'
    text = path.read_text()
    if name == 'stop-at-lost-reply':
        old = '\t\t(void)record(f, request, APPLY, records, pick, k, &ok);'
        new = '\t\tif (!record(f, request, APPLY, records, pick, k, &ok)) break;'
        selected = 'Face.ALostReply*'
        expected = [(t, agreement) for t in (
            'Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing',
            'Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing')]
    else:
        old = 'records + 8u * (pick != NULL ? pick[k] : k)'
        new = 'records + 8u * (pick != NULL ? k : k)'
        selected = 'Face.AnEditCommitsTheMappingsTheCorePicksAndNoOthers'
        expected = [(selected, 'the records the core picked are committed')]
    assert text.count(old) == 1
    path.write_text(text.replace(old, new))

tree = Tree(src, scratch / 'build', scratch / 'reuse', fw_gtest.Build(jobs=4), STACK)
result = aecp_arms.core_arm(tree, repo / 'configs/endstation_ax7101_1x1_tdm8.yaml',
                            interfaces, mode, selected)
print(result.log)
print('Suite exit:', result.rc)
if expected:
    ok = result.rc != 0 and all('[FAIL] ' + test + ': ' + words in result.log for test, words in expected)
else:
    ok = result.rc == 0 and '164 tests' in result.log
print('PROBE', name, 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
