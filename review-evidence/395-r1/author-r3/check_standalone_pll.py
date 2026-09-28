"""Prove the standalone entry executes the PLL control without editing the lane."""
from pathlib import Path
import subprocess
import sys

ROOT = Path('$LANES/395-timing-grade')
LITEX = '$WORKSPACE_HOME/litex-milan/venv/bin/python3'
ENTRY = ROOT / 'sw/builder/test_timing_grade.py'
GOOD = 'declared part reaches the AX7101 PLL speed grade, including a changed-part control'

# The child imports a modified module in memory, keeping its real __file__ so
# that source and submodule discovery still use the registered physical lane.
PRELOAD = '''
import pathlib, sys, types
p = pathlib.Path('milan_soc.py').resolve()
source = p.read_text()
old = 'S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))'
assert source.count(old) == 1
source = source.replace(old, 'S7PLL(speedgrade=-2)')
module = types.ModuleType('milan_soc')
module.__file__ = str(p)
sys.modules['milan_soc'] = module
exec(compile(source, str(p), 'exec'), module.__dict__)
'''

BOOTSTRAP = r'''
import runpy, subprocess, sys
from unittest.mock import patch
real_run = subprocess.run
def run(argv, *args, **kwargs):
    if '-c' in argv and 'import milan_soc' in argv[-1]:
        argv = list(argv)
        argv[-1] = PRELOAD + '\n' + argv[-1]
    return real_run(argv, *args, **kwargs)
sys.argv = [ENTRY, LITEX]
with patch.object(subprocess, 'run', side_effect=run):
    runpy.run_path(ENTRY, run_name='__main__')
'''

control = subprocess.run([sys.executable, '-B', str(ENTRY), LITEX], cwd=ROOT,
                         capture_output=True, text=True, timeout=300, check=False)
print('CONTROL rc=' + str(control.returncode))
print(control.stdout)
assert control.returncode == 0 and GOOD in control.stdout, control.stderr
script = f'PRELOAD = {PRELOAD!r}\nENTRY = {str(ENTRY)!r}\nLITEX = {LITEX!r}\n' + BOOTSTRAP
mutant = subprocess.run([sys.executable, '-B', '-c', script], cwd=ROOT,
                        capture_output=True, text=True, timeout=300, check=False)
print('PLL LITERAL MUTANT rc=' + str(mutant.returncode))
print(mutant.stdout)
print(mutant.stderr)
assert mutant.returncode == 1 and 'AssertionError: call(speedgrade=-2)' in mutant.stderr
assert 'test_pll_grade(sys.argv[1])' in mutant.stderr
print('PASS: the standalone entry reaches the changed-part assertion and kills the literal.')
