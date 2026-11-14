"""An ad hoc plant on a scratch copy of the firmware tree, run through aecp_arms.core_arm in mailbox mode at a
configuration and interface count: prints its tests' outcome, or the build's refusal and the words it was refused by.
usage: python3 -B adhoc_plant.py LANE SCRATCH FILE OLD NEW CONFIG INTERFACES FILTER WORDS"""
import shutil
import sys
from pathlib import Path

lane, scratch, file, old, new, config, interfaces, selected, words = sys.argv[1:10]
sys.path.insert(0, str(Path(lane) / 'sw/firmware/ctrl/test'))
import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal  # noqa: E402

scratch = Path(scratch)
src = scratch / 'work/ctrl'
shutil.rmtree(scratch / 'work', ignore_errors=True)
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', ignore=shutil.ignore_patterns('test', '__pycache__', '*.pyc'))
target = src / file
text = target.read_text()
assert text.count(old) == 1, f'{text.count(old)} planting sites'
target.write_text(text.replace(old, new))
print(f'# ad hoc plant in {file}: {old!r} -> {new!r}; {Path(config).name} at {interfaces} interface(s), mailbox mode')
tree = Tree(src, scratch / 'work/build', scratch / 'work/reuse', fw_gtest.Build(jobs=8), STACK)
try:
    result = aecp_arms.core_arm(tree, ROOT / config, int(interfaces), 'mailbox', selected)
    log, refused = result.log, False
except Refusal as error:
    log, refused = str(error), True
hits = [line for line in log.splitlines() if words in line]
print('the build refused' if refused else f'the tests ran: rc {result.rc}')
print('\n'.join(line.replace(str(scratch), '<scratch>') for line in hits[:4]))
print(('CAUGHT' if hits else 'ESCAPED') + f' by the words {words!r}')
sys.exit(0 if hits else 1)
