#!/usr/bin/env python3
"""Independently replay the named plants and the old production code controls."""
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import aecp_arms as arms
import aecp_mutants as mutants
import aecp_output_mutants as outputs
from ctrl_build import CTRL, Tree, fw_gtest

def tree_for(name):
    work = packet / 'scratch' / name
    src = work / 'ctrl'
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(CTRL.parent / 'ctrl_nvm', work / 'ctrl_nvm', dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('test', '__pycache__'))
    return Tree(src, work / 'build', work / 'reuse', fw_gtest.Build(jobs=4))

def plants():
    mutants.controls()
    tree = tree_for('plants')
    rows = [mutants.defect(*r) for r in outputs.ROWS]
    rows += [d for d in mutants.DEFECTS if d.name == 'stream-read-brief']
    receipts = []
    for d in rows:
        path = tree.src / d.path
        original = path.read_text()
        assert original.count(d.old) == 1, d.name
        try:
            path.write_text(original.replace(d.old, d.new))
            result = arms.core_arm(tree, repo / 'configs/endstation_ax7101_1x1_tdm8.yaml', 2,
                                   'app', ':'.join(t for t, _ in d.checks))
            (packet / ('plant-' + d.name + '.log')).write_text(result.log)
            passed = all(mutants.caught(test, words, result) for test, words in d.checks)
            receipts.append({'plant': d.name, 'caught': passed, 'rc': result.rc, 'checks': d.checks})
            print(d.name, 'caught' if passed else 'ESCAPED', flush=True)
        finally:
            path.write_text(original)
    (packet / 'plants.json').write_text(json.dumps(receipts, indent=2) + '\n')
    return 0 if all(r['caught'] for r in receipts) else 1

def base(shape):
    tree = tree_for('old-code-' + shape)
    paths = ['app/ctrl_app_aecp.c', 'aecp/aecp_commands.c', 'aecp/aecp_internal.h', 'aecp/aecp_maps.c']
    for path in paths:
        (tree.src / path).write_bytes(subprocess.check_output(
            ['git', 'show', '0839453f:sw/firmware/ctrl/' + path], cwd=repo))
    config = 'endstation_ax7101_1x1_tdm8.yaml' if shape == '1x1' else 'endstation_ax7101_8x8.yaml'
    selected = 'AppOutputs.*:Core.TheRunningCheckObservesEveryStreamBriefly:Core.*Map*:Face.TheRunningCheckReadsOneWindowWordAStream'
    result = arms.core_arm(tree, repo / 'configs' / config, 1, 'app', selected)
    (packet / ('old-code-' + shape + '.log')).write_text(result.log)
    (packet / ('old-code-' + shape + '.rc')).write_text(str(result.rc) + '\n')
    expected = mutants.caught(outputs.TEST, "a declaring STREAM_OUTPUT's stream_dest_mac is its Talker's MAAP address", result)
    print('old-code', shape, 'fails by name', expected, flush=True)
    return 0 if expected else 1

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(plants), pool.submit(base, '1x1'), pool.submit(base, '8x8')]
    results = [f.result() for f in futures]
raise SystemExit(max(results))
