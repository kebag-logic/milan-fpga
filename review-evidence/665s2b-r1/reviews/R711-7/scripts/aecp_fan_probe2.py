#!/usr/bin/env python3
"""Plant reviewer defects (and the author's four lost-frame defects) into a scratch copy of the AECP tree and run the
AECP core arm in app mode at two interfaces over the whole suite; report which tests fail for each.
usage: python3 -I aecp_fan_probe.py <tree> <scratch-out>"""
import re, shutil, sys
from pathlib import Path
tree_root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(tree_root / 'sw/firmware/ctrl/test'), str(tree_root / 'sw/firmware/gtest')]
import aecp_arms, fw_gtest
from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal
PLANTS = [
    ('refused-mid-fan-after-a-taken-frame-taken-as-lost', 'aecp/aecp.c', '\t\t\t\tlost = taken == AECP_FAN_LOST;\n', '\t\t\t\tlost = taken == AECP_FAN_LOST || held_r != NULL;\n'),
]
PLANTS_ALL = [
    ('none', None, None, None),
    # reviewer: a refused frame (no room) resumed as if lost, at the recipient before it: a duplicate delivery
    ('refused-mid-fan-taken-as-lost', 'aecp/aecp.c', '\t\t\t\tlost = taken == AECP_FAN_LOST;\n', '\t\t\t\tlost = true;\n'),
    # reviewer: fan_end's refusal (no room for the completion) resumed as if its last frame were lost
    ('fan-end-refused-taken-as-lost', 'aecp/aecp.c', '\t\tlost = lost || end == AECP_FAN_LOST;\n',
     '\t\tlost = lost || end != AECP_FAN_TAKEN;\n'),
    # the author's four (aecp_fan_mutants.py)
    ('notice-lost-frame-skipped', 'aecp/aecp.c', '\t\t\t\tlost = taken == AECP_FAN_LOST;\n', '\t\t\t\tlost = false;\n'),
    ('notice-lost-frame-sequence-spent', 'aecp/aecp.c', '\t\t--held_r->sequence;\n', '\t\t(void)held_r;\n'),
    ('notice-lost-last-frame-dropped', 'aecp/aecp.c', '\t\tlost = lost || end == AECP_FAN_LOST;\n', ''),
    ('notice-lost-frame-resumed-at-the-next', 'aecp/aecp.c', '\t\t\t\theld = k;\n', '\t\t\t\theld = k + 1u;\n'),
]
out.mkdir(parents=True, exist_ok=True)
src = out / 'work/ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
tree = Tree(src, out / 'work/build', out / 'work/reuse', fw_gtest.Build(jobs=8), STACK)
config = ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
for name, path, old, new in PLANTS:
    target = src / path if path else None
    original = target.read_text() if target else None
    if target:
        assert original.count(old) == 1, name
        target.write_text(original.replace(old, new))
    try:
        r = aecp_arms.core_arm(tree, config, 2, 'app', '*')
        failed = sorted(set(re.findall(r'\[  FAILED  \] (\S+) \(', r.log)))
        (out / f'{name}.log').write_text(r.log)
        print(f'{name}: rc {r.rc}, failed tests {len(failed)}: {", ".join(failed) or "-"}', flush=True)
    except Refusal as e:
        print(f'{name}: REFUSED {str(e)[:300]}', flush=True)
    finally:
        if target:
            target.write_text(original)
