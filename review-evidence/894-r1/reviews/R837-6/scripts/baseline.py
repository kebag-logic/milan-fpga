#!/usr/bin/env python3
"""Unplanted baseline of the AECP core suites at a tree, in the campaign's isolated copy: the app arm (Core.*,
Mailbox.*) and the work arm (Core.MapEditWork*). usage: baseline.py TREE OUT"""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / 'sw/firmware/ctrl/test'), str(tree / 'sw/firmware/gtest')]
import shutil  # noqa: E402
import aecp_mutants as am  # noqa: E402
import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402
out = Path(sys.argv[2]).resolve()
src = out / 'work/ctrl'
shutil.copytree(am.CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(am.CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
t = am.Tree(src, out / 'work/build', out / 'work/reuse', fw_gtest.Build(jobs=4), (tree / 'third_party/tsn-c-stack').resolve())
config = am.ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
rc = 0
for arm, n, sel in (('app', 2, 'Core.*:Mailbox.*'), ('work', 1, 'Core.MapEditWork*')):
    r = aecp_arms.core_arm(t, config, n, arm, sel)
    (out / f'{arm}.log').write_text(r.log)
    tail = [l for l in r.log.splitlines() if l.startswith('[  PASSED  ]') or l.startswith('[  FAILED  ]') or 'tests ran' in l]
    print(arm, *tail[-3:], sep='\n  ')
    rc |= any(l.startswith('[  FAILED  ]') for l in tail)
sys.exit(rc)
