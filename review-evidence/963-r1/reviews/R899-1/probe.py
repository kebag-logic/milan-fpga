#!/usr/bin/env python3
"""Focused disposable probes. Usage: probe.py CHECKOUT PACKET"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_arms as arms
import aecp_mutants as mutants
import fw_gtest
from ctrl_build import CTRL, STACK, Tree

scratch = packet / 'scratch/probe'
src = scratch / 'ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True)
config = root / 'configs/endstation_ax7101_1x1_tdm8.yaml'
build = fw_gtest.Build(jobs=4)
tree = Tree(src, scratch / 'build', scratch / 'reuse', build, STACK)
mapping = src / 'aecp/aecp_maps.c'
head = mapping.read_text()
base = subprocess.check_output(['git', '-C', str(root), 'show',
    'dd163e41438acb86e0c4d4e76df90f3f91ace1c0:sw/firmware/ctrl/aecp/aecp_maps.c'], text=True)
results = []
selected = 'Core.MapEditsAreTheirDefinitionRowForRow:Core.MapEditWorkObservesEachOutputStreamOnce'
for name, code in [('head', head), ('base', base)]:
    mapping.write_text(code)
    result = arms.core_arm(tree, config, 2, 'core', selected)
    (packet / f'probe-{name}.log').write_text(result.log)
    assert result.rc == (0 if name == 'head' else 1)
    results.append(dict(case=name, rc=result.rc))
mapping.write_text(head)
mutants.controls()
names = {'map-port-rows-unread', 'map-owners-unread', 'map-checked-before-its-read',
         'map-stream-observed-every-mapping', 'map-stream-idle-uncleared',
         'map-stream-idle-one-bit', 'map-stream-running-accepted', 'map-idle-reads-whole'}
for defect in mutants.DEFECTS:
    if defect.name not in names:
        continue
    assert defect.path == 'aecp/aecp_maps.c'
    assert head.count(defect.old) == 1
    mapping.write_text(head.replace(defect.old, defect.new))
    result = arms.core_arm(tree, config, 2, 'core', ':'.join(test for test, _ in defect.checks))
    caught = all(mutants.caught(test, words, result) for test, words in defect.checks)
    (packet / f'probe-{defect.name}.log').write_text(result.log)
    results.append(dict(case=defect.name, caught=caught, rc=result.rc))
    assert caught, defect.name
mapping.write_text(head)

# A separate test documents the deliberately different response when the
# environment would stop answering the second mapping's observation.
extra = r'''
TEST_F(Core, ReviewObservationFailureAfterFirstRead)
{
    unsigned calls=0;
    ON_CALL(mock,Stream).WillByDefault([&](unsigned,uint16_t,uint16_t,aecp_stream_info *v){
        EXPECT_TRUE(v->brief);
        EXPECT_FALSE(v->running); // aecp_stream_read must initialize it
        ++calls;
        return calls==1;
    });
    const aecp_mapping a{0,0,0,0},b{0,1,1,0};
    edit_map(44,15,{a,b},EXPECTED_STATUS);
    EXPECT_EQ(calls,EXPECTED_CALLS);
    EXPECT_EQ(maps[1].count,EXPECTED_ROWS);
}
'''
arms.HERE = src / 'test'
tests = (CTRL / 'test/test_aecp.cpp').read_text()
for name, code, status, calls, rows in [('head', head, 0, 1, 2), ('base', base, 7, 2, 0)]:
    mapping.write_text(code)
    added = extra.replace('EXPECTED_STATUS', str(status)).replace('EXPECTED_CALLS', str(calls)+'u').replace('EXPECTED_ROWS', str(rows)+'u')
    (arms.HERE / 'test_aecp.cpp').write_text(tests + added)
    result = arms.core_arm(tree, config, 2, 'core', 'Core.ReviewObservationFailureAfterFirstRead')
    (packet / f'probe-later-unanswered-{name}.log').write_text(result.log)
    assert result.rc == 0
    results.append(dict(case='later-unanswered-'+name, status=status, reads=calls, rows=rows, rc=result.rc))
mapping.write_text(head)
(packet / 'probe-results.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))
