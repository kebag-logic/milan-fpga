"""Check documented CLI requirements and prove runtime defaults unchanged."""
import ast
import contextlib
import io
from pathlib import Path
import shlex
import subprocess
import sys
from unittest.mock import patch

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT / 'sw/builder'))
sys.path.insert(0, str(ROOT / 'sw/litex'))
import endstation_builder as eb
import milan_soc
import test_clock_contract as contract

source = (ROOT / 'sw/litex/milan_soc.py').read_text()
base = subprocess.run(['git', 'show', '3baff441:sw/litex/milan_soc.py'],
                      check=True, capture_output=True, text=True).stdout


def without_help(text):
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'add_argument':
            node.keywords = [kw for kw in node.keywords if kw.arg != 'help']
    return ast.dump(tree, include_attributes=False)


assert without_help(source) == without_help(base), 'runtime/default change in documentation item'
print('PASS: SoC executable AST differs only in argument help; every default is unchanged')
header = source.split('\nimport os', 1)[0]
assert '--milan-clk-freq <CPU_HZ>' in header
assert 'tb/verilator/nvm_capture_cpu/recipe.py' in header
assert '--entity-gen-dir configs/generated/<cfg>' in header
header = header.replace('\\\n#       ', ' ')
count = 0
for line in header.splitlines():
    if not line.startswith('#   ./milan_soc.py'):
        continue
    argv = shlex.split(line[2:].strip(), comments=True)[1:]
    argv += ['--milan-clk-freq', str(eb.BAREMETAL_CLK_HZ)]
    if '--no-milan' not in argv:
        argv += ['--entity-gen-dir', 'configs/generated/endstation_ax7101_1x1_tdm8']
    contract._soc_clock_case(milan_soc, argv, False)
    count += 1
print(f'PASS: {count} header invocations plus their stated required options reach the platform boundary')
help_output = io.StringIO()
with patch.object(sys, 'argv', ['milan_soc.py', '--help']), contextlib.redirect_stdout(help_output):
    try:
        milan_soc.main()
    except SystemExit as exc:
        assert exc.code == 0
help_text = ' '.join(help_output.getvalue().split())
assert help_text.count('CPU_HZ in tb/verilator/nvm_capture_cpu/recipe.py') == 2
assert 'There is no tracked entity fallback' in help_text
print('PASS: both clock help entries cite the single definition; entity help requires generated artifacts')
reference = (ROOT / 'sw/builder/README-parameters.md').read_text().split('## Product profile', 1)[1].split('\n## ', 1)[0]
assert '`board.constraints.milan_clk_hz`' in reference and '`CPU_HZ`' in reference
assert 'Fixed' in reference
for line in (ROOT / 'docs/ENDSTATION_BUILDER.md').read_text().splitlines():
    if line.startswith(('| 5a |', '| 34 |')):
        assert 'Milan clock is fixed to `CPU_HZ`' in line and '../tb/verilator/nvm_capture_cpu/recipe.py' in line
print('PASS: parameter table and rows 5a/34 state the fixed clock by reference')
