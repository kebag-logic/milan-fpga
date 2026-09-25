from pathlib import Path
import subprocess
from run_gate import ROOT, run

BASE = '864b36f5e9450ef64f75ca3f0d68c44330e447d7'
paths = subprocess.check_output(['git', 'diff', '--name-only', BASE, 'HEAD', '--', 'hdl', 'configs/generated'], cwd=ROOT, text=True).splitlines()
assert all(p.endswith(('.sv', '.svh')) for p in paths)
original = {p: (ROOT / p).read_bytes() for p in paths}
recipe = ROOT / 'syn/yosys/ooc.sh'
recipe_bytes = recipe.read_bytes()
anchor = '  "milan_datapath|$DP_SRCS"\n'
assert recipe_bytes.decode().count(anchor) == 1
extended = recipe_bytes.decode().replace(anchor, anchor + '  "milan_csr|$R/hdl/common/csr/milan_csr.sv"\n')
try:
    recipe.write_text(extended)
    for p in paths:
        (ROOT / p).write_bytes(subprocess.check_output(['git', 'show', BASE + ':' + p], cwd=ROOT))
    assert run('ooc-base', ['bash', 'syn/yosys/ooc.sh', 'milan_csr', 'KL_pp_shadow', 'milan_datapath']) == 0
    for p, data in original.items():
        (ROOT / p).write_bytes(data)
    assert run('ooc-head-csr', ['bash', 'syn/yosys/ooc.sh', 'milan_csr']) == 0
finally:
    for p, data in original.items():
        (ROOT / p).write_bytes(data)
    recipe.write_bytes(recipe_bytes)
assert all((ROOT / p).read_bytes() == data for p, data in original.items())
assert recipe.read_bytes() == recipe_bytes
