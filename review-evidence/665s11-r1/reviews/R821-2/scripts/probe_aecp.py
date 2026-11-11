#!/usr/bin/env python3
"""Reviewer probe: plant one edit into a scratch copy of sw/firmware/ctrl as aecp_mutants.campaign does, and run
the AECP core arm (app mode, two interfaces) on the REBOOT tests. Usage: probe_aecp.py <repo-root> <scratch> <mode>
mode: head | handover"""
import shutil, sys
from pathlib import Path
root, scratch, mode = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import aecp_arms, fw_gtest                                    # noqa: E402
from ctrl_build import Tree                                   # noqa: E402
CTRL = root / 'sw/firmware/ctrl'
src = scratch / 'work/ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
if mode == 'handover':
    t = src / 'aecp/aecp.c'
    text = t.read_text()
    assert text.count('\treturn a->reboot != 0u;\n') == 1
    t.write_text(text.replace('\treturn a->reboot != 0u;\n', '\treturn a->reboot >= 2u;\n'))
tree = Tree(src, scratch / 'work/build', scratch / 'work/reuse', fw_gtest.Build(jobs=4))
o = aecp_arms.core_arm(tree, root / 'configs/endstation_ax7101_1x1_tdm8.yaml', 2, 'app', 'Core.Reboot*')
print(f'PROBE aecp {mode}: rc {o.rc}')
for ln in o.log.splitlines():
    if '[FAIL]' in ln or '[       OK ]' in ln or 'PASSED' in ln or 'FAILED' in ln:
        print('    ' + ln.strip()[:300])
