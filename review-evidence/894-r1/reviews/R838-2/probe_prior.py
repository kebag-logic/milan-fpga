#!/usr/bin/env python3
"""Run the two earlier test-gap regressions and their exact planted defects."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
if len(sys.argv) == 2:
    def run(kind):
        p = subprocess.run([sys.executable, '-B', __file__, str(root), kind],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (packet/'checks'/f'prior_{kind}.log').write_text(p.stdout)
        (packet/'checks'/f'prior_{kind}.rc').write_text(f'{p.returncode}\n')
        print(f'{kind}: rc={p.returncode}', flush=True)
        return p.returncode
    with ThreadPoolExecutor(max_workers=2) as pool:
        codes = list(pool.map(run, ('owed', 'round')))
    raise SystemExit(any(codes))

kind = sys.argv[2]
sys.path.insert(0, str(root/'sw/firmware/ctrl/test'))
import aecp_arms
import ctrl_arms
import ctrl_build
import fw_gtest

if kind == 'owed':
    selected = 'Queued.AfterTheQueuesLastNoticeTheLongerOneIsStillOwed'
    relative = 'aecp/aecp.c'
    before = '\t\treturn a->owed_count != 0u || a->notify;\n'
    after = '\t\treturn a->owed_count != 0u;\n'
    words = 'and runs no lock expiry beside it'
else:
    selected = 'Loop.L28AnOrdinaryPassesRoundIsToldItStandsAlone'
    relative = 'loop/ctrl_loop.c'
    before = '\t\tl->round_one = false;\n\t\towed = round_of(l, slice_end(l, deadline)) || owed;\n'
    after = '\t\towed = round_of(l, slice_end(l, deadline)) || owed;\n'
    words = "L28 an ordinary pass's round is told it stands alone"
    os.environ['GTEST_FILTER'] = selected

for mutant in (False, True):
    place = packet/'scratch/prior'/kind/('mutant' if mutant else 'baseline')
    src = place/'ctrl'
    shutil.copytree(root/'sw/firmware/ctrl', src, dirs_exist_ok=True)
    if mutant:
        p = src/relative
        text = p.read_text()
        assert text.count(before) == 1
        p.write_text(text.replace(before, after))
    tree = ctrl_build.Tree(src, place/'build', place/'reuse', fw_gtest.Build(jobs=6))
    if kind == 'owed':
        result = aecp_arms.core_arm(tree, root/'configs/endstation_ax7101_1x1_tdm8.yaml',
                                   1, 'core', selected)
    else:
        result = ctrl_arms.arm_port(tree)
    print(f'mutant={mutant} rc={result.rc}\n{result.log}', flush=True)
    assert (result.rc != 0) == mutant
    if mutant:
        assert words in result.log
print('PASS: baseline passes; the earlier missing assertion now catches its planted defect.')
