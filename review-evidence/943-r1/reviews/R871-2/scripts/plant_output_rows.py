#!/usr/bin/env python3
"""Plant each row of aecp_output_mutants.ROWS alone in a scratch copy of the control firmware and run the named
tests on it at one shape and interface count; a row is caught when every named check fails on its own words.

usage: python3 -I plant_output_rows.py CLONE OUT CONFIG_STEM INTERFACES [ROW ...]
The clone is read, never written: the firmware is copied under OUT (aecp_mutants.campaign's method)."""
import json
import shutil
import sys
from pathlib import Path

clone, out, stem, ifs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
only = set(sys.argv[5:])
sys.path.insert(0, str(clone / 'sw/firmware/ctrl/test'))
import aecp_arms  # noqa: E402
import aecp_mutants  # noqa: E402
import aecp_output_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
src = out / 'work/ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
tree = Tree(src, out / 'work/build', out / 'work/reuse', fw_gtest.Build(jobs=4), STACK.resolve())
config = ROOT / f'configs/{stem}.yaml'
names = {row[0] for row in aecp_output_mutants.ROWS}
rows = [d for d in aecp_mutants.DEFECTS if d.name in names and (not only or d.name in only)]
receipts, escaped = [], 0
# the unplanted tree first: every named test passes
base = aecp_arms.core_arm(tree, config, ifs, 'app', ':'.join(sorted({t for d in rows for t, _ in d.checks})))
(out / 'unplanted.log').write_text(base.log)
print(f'unplanted {stem} if{ifs}: rc {base.rc}', flush=True)
for d in rows:
    target = src / d.path
    original = target.read_text()
    if original.count(d.old) != 1:
        raise Refusal(f'{d.name}: expected one planting site, got {original.count(d.old)}')
    target.write_text(original.replace(d.old, d.new))
    try:
        result = aecp_arms.core_arm(tree, config, ifs, 'app', ':'.join(t for t, _ in d.checks))
        ok = all(aecp_mutants.caught(t, w, result) for t, w in d.checks)
        (out / (d.name + '.log')).write_text(result.log)
    finally:
        target.write_text(original)
    escaped += not ok
    receipts.append({'row': d.name, 'caught': ok, 'rc': result.rc, 'words': [w for _, w in d.checks]})
    print(f"[{'ok' if ok else 'ESCAPED'}] {d.name} rc={result.rc}", flush=True)
(out / 'results.json').write_text(json.dumps(receipts, indent=2) + '\n')
print(f'{stem} if{ifs}: {len(rows)} planted, {escaped} escaped, unplanted rc {base.rc}')
sys.exit(1 if escaped or base.rc else 0)
