#!/usr/bin/env python3
"""Run a focused native baseline and three diagnostic-checked mutations.
Usage: python3 probe_configuration.py REPOSITORY PACKET
Builds and source copies stay in PACKET/scratch; two builds of eight jobs each.
"""
import concurrent.futures
import json
import pathlib
import shutil
import sys

root, packet = map(pathlib.Path, sys.argv[1:])
sys.path.insert(0, str(root/'sw/firmware/ctrl/test'))
import aecp_arms
import aecp_mutants
import ctrl_build
import fw_gtest

out = packet/'configuration'
out.mkdir(exist_ok=True)
config = root/'configs/endstation_ax7101_1x1_tdm8.yaml'
names = ('running-reads-no-word', 'configuration-streams-every-time', 'configuration-unpaced')
plants = {d.name: d for d in aecp_mutants.DEFECTS if d.name in names}
baseline = ':'.join((
    'Core.ConfigurationAndLockedSetRefusals',
    'Core.TheRunningCheckObservesEveryStreamBriefly',
    'Core.AConfigurationChangeNamesWhetherItsIndexMoved',
    'Face.TheRunningCheckReadsOneWindowWordAStream',
    'Face.OnlyAMovedConfigurationIndexWritesTheStreamEntries',
    'Face.ALateCommitIsOwedAndPublishedAgainWhole',
    'Face.EachSettingIsCommittedBeforeTheResponseThatPromisesIt',
    'Mailbox.AnAcceptedConfigurationHoldsTheNextRecordForThePace'))

def run(name):
    work = packet/'scratch/configuration'/name
    src = work/'ctrl'
    shutil.copytree(root/'sw/firmware/ctrl', src, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    shutil.copytree(root/'sw/firmware/ctrl_nvm', work/'ctrl_nvm', ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
    d = plants.get(name)
    if d:
        p = src/d.path
        text = p.read_text()
        assert text.count(d.old) == 1
        p.write_text(text.replace(d.old, d.new))
    tree = ctrl_build.Tree(src, work/'build', work/'reuse', fw_gtest.Build(jobs=8), ctrl_build.STACK)
    selected = ':'.join(t for t, _ in d.checks) if d else baseline
    try:
        result = aecp_arms.core_arm(tree, config, 2, 'app', selected)
        # Preserve diagnostics while making local paths portable.
        (out/(name+'.log')).write_text(result.log.replace(str(packet), '<review-packet>').replace(str(root)+'/', ''))
        ok = all(aecp_mutants.caught(t, words, result) for t, words in d.checks) if d else result.rc == 0
        row = {'name': name, 'rc': result.rc, 'accepted': ok, 'selected': selected}
    except Exception as error:
        row = {'name': name, 'accepted': False, 'error': str(error).replace(str(packet), '<review-packet>')}
    print(json.dumps(row), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, ('baseline', *names)))
(out/'results.json').write_text(json.dumps(results, indent=2)+'\n')
sys.exit(not all(r['accepted'] for r in results))
