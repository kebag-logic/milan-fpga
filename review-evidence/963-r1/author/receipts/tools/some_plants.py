#!/usr/bin/env python3
"""some_plants.py CTRL_TEST_DIR OUT NAME...: run the named rows of the AECP campaign's table (aecp_mutants.DEFECTS)
exactly as aecp_mutants.campaign runs each, in an isolated copy, and print [ok] or [ESCAPED] by the campaign's own
caught() and refused() rules."""
import shutil
import sys
from pathlib import Path

here = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(here))
import aecp_arms  # noqa: E402
import aecp_mutants as m  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Refusal, Tree  # noqa: E402

out, names = Path(sys.argv[2]), sys.argv[3:]
chosen = [d for d in m.DEFECTS if d.name in names]
assert {d.name for d in chosen} == set(names), set(names) - {d.name for d in chosen}
m.controls()
src = out / 'work/ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
tree = Tree(src, out / 'work/build', out / 'work/reuse', fw_gtest.Build(jobs=4), STACK)
config = ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml'
bad = 0
for d in chosen:
    target = src / d.path
    original = target.read_text()
    assert original.count(d.old) == 1, (d.name, original.count(d.old))
    target.write_text(original.replace(d.old, d.new))
    try:
        selected = ':'.join(test for test, _ in d.checks)
        work = d.checks[0][0].startswith(aecp_arms.WORK.rstrip('*'))
        result = (aecp_arms.core_arm(tree, config, 1, 'work', selected) if work else
                  aecp_arms.core_arm(tree, config, 2, 'app', selected))
        ok = all(m.caught(test, words, result) for test, words in d.checks)
        (out / (d.name + '.log')).write_text(result.log)
    except Refusal as error:
        ok = m.refused(d, str(error))
        (out / (d.name + '.log')).write_text(str(error))
    finally:
        target.write_text(original)
    bad += not ok
    print(f"[{'ok' if ok else 'ESCAPED'}] {d.name}: {selected}", flush=True)
sys.exit(1 if bad else 0)
