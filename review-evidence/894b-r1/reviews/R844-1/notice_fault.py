"""One AECP campaign plant run as aecp_mutants.campaign runs each (a scratch copy of the firmware tree and the store
beside it, the plant applied once, its named tests on the shipping configuration at two interfaces in app mode, caught
only by each test's own failure words), and again at another configuration and interface count in mailbox mode.
usage: python3 -B one_aecp_plant.py LANE SCRATCH NAME [CONFIG INTERFACES]   (run with the lane's tool environment)"""
import shutil
import sys
from pathlib import Path

lane, scratch, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(lane / 'sw/firmware/ctrl/test'))
import aecp_arms  # noqa: E402
import aecp_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal  # noqa: E402

defect = next(d for d in aecp_mutants.DEFECTS if d.name == name)
config = ROOT / (sys.argv[4] if len(sys.argv) > 4 else 'configs/endstation_ax7101_1x1_tdm8.yaml')
interfaces = int(sys.argv[5]) if len(sys.argv) > 5 else 2
mode = 'app' if len(sys.argv) <= 4 else 'mailbox'
src = scratch / 'work/ctrl'
shutil.rmtree(scratch / 'work', ignore_errors=True)
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
target = src / defect.path
original = target.read_text()
assert original.count(defect.old) == 1, f'{name}: {original.count(defect.old)} planting sites'
target.write_text(original.replace(defect.old, defect.new))
tree = Tree(src, scratch / 'work/build', scratch / 'work/reuse', fw_gtest.Build(jobs=8), STACK)
selected = ':'.join(test for test, _ in defect.checks)
try:
    result = aecp_arms.core_arm(tree, config, interfaces, mode, selected)
    caught = {test: aecp_mutants.caught(test, words, result) for test, words in defect.checks}
except Refusal as error:
    result, caught = None, {test: False for test, _ in defect.checks}
    print('REFUSED', error)
print(f'# plant {name} ({defect.path}), {config.name} at {interfaces} interface(s), {mode} mode, tests {selected}')
if result is not None:
    lines = result.log.splitlines()
    print('\n'.join(line for line in lines if line.startswith(('[ RUN', '[  FAILED', '[       OK', '  verdict'))
                    or 'Failure' in line or 'none dropped' in line or 'Expected' in line or 'Which is' in line))
for test, ok in caught.items():
    print(f'{"CAUGHT" if ok else "ESCAPED"} {name}: {test} by its words {dict(defect.checks)[test]!r}')
sys.exit(0 if all(caught.values()) else 1)
