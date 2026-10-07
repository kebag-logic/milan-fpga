#!/usr/bin/env python3
"""Reconstruct the series; exercise the committed test with independent plants."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
env = dict(os.environ, PYTHON=sys.executable, MILAN_LITEX_PYTHON=sys.executable,
           PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', TMPDIR=str(scratch))
os.environ.update(env)
import liteeth.phy.gmii as gmii
import litex
import pythondata_cpu_vexiiriscv as cpu

core = Path(litex.__file__).parent / 'soc/cores/cpu/vexiiriscv/core.py'
sha = re.search(r'git_setup\("VexiiRiscv".*?"([0-9a-f]{40})"', core.read_text()).group(1)
soc = Path(cpu.data_location) / 'ext/VexiiRiscv/src/main/scala/vexiiriscv/soc/litex/Soc.scala'
soc.parent.mkdir(parents=True, exist_ok=True)
soc.write_bytes(urllib.request.urlopen(f'https://raw.githubusercontent.com/SpinalHDL/VexiiRiscv/{sha}/src/main/scala/vexiiriscv/soc/litex/Soc.scala', timeout=120).read())
(packet / 'cpu-patch-input.json').write_text(json.dumps({'commit': sha, 'Soc.scala_sha256': hashlib.sha256(soc.read_bytes()).hexdigest()}, indent=2)+'\n')
original = (scratch / 'deps/liteeth/liteeth/phy/gmii.py').read_text()
(scratch / 'original-gmii.py').write_text(original)
apply = repo / 'sw/litex/patches/apply.sh'
for label, args in [('apply-first', []), ('apply-idempotent', []), ('apply-reverse', ['--reverse']), ('apply-final', [])]:
    r = subprocess.run(['bash', str(apply), *args], env=env, capture_output=True, text=True)
    (packet / f'{label}.log').write_text(r.stdout.replace(str(scratch), '$SCRATCH')+r.stderr.replace(str(scratch), '$SCRATCH'))
    assert r.returncode == 0, (label, r.stderr)
    if label == 'apply-first':
        patched = Path(gmii.__file__).read_text()
    elif label == 'apply-reverse':
        assert Path(gmii.__file__).read_text() == original
    else:
        assert Path(gmii.__file__).read_text() == patched

controls = {
    'candidate': patched,
    'original': original,
    'live-reset': patched.replace('rx_dv & ~rx_reset', 'rx_dv & ~ResetSignal()'),
    'missing-last': patched.replace('source.last.eq(~pads.rx_dv & source.valid)', 'source.last.eq(0)'),
    'data-bit-lost': patched.replace('rx_data.eq(pads.rx_data)', 'rx_data.eq(pads.rx_data & 0x7f)'),
}
program = '''import sys, types, runpy
from pathlib import Path
import liteeth.phy.gmii
module = types.ModuleType('liteeth.phy.gmii')
exec(compile(Path(sys.argv[1]).read_text(), sys.argv[1], 'exec'), module.__dict__)
sys.modules['liteeth.phy.gmii'] = module
sys.argv = [sys.argv[2]]
runpy.run_path(sys.argv[0], run_name='__main__')
'''
test = repo / 'sw/litex/test_gmii_rx_capture.py'
def check(item):
    label, source = item
    src = scratch / f'gmii-{label}.py'
    src.write_text(source)
    r = subprocess.run([sys.executable, '-c', program, str(src), str(test)], env=env, capture_output=True, text=True)
    output = (r.stdout+r.stderr).replace(str(repo), '$REPO').replace(str(scratch), '$SCRATCH')
    (packet / f'capture-{label}.log').write_text(output)
    (packet / f'capture-{label}.rc').write_text(str(r.returncode)+'\n')
    if label in ('candidate', 'original'):
        assert r.returncode == 0 and '1036' in output and 'RESULT: PASS' in output
    else:
        assert source != patched and r.returncode != 0 and 'AssertionError:' in output
    return {'case': label, 'returncode': r.returncode, 'expected_outcome_observed': True}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(check, controls.items()))
(packet / 'capture-controls.json').write_text(json.dumps(results, indent=2)+'\n')
code = "import sys; sys.path.insert(0,'sw/builder'); import test_builder as t; t.test_toolchain_patches_are_applied(); t.test_toolchain_patch_gate_bites()"
r = subprocess.run([sys.executable, '-c', code], cwd=repo, env=env, capture_output=True, text=True)
(packet / 'patch-gates.log').write_text((r.stdout+r.stderr).replace(str(scratch), '$SCRATCH'))
(packet / 'patch-gates.rc').write_text(str(r.returncode)+'\n')
assert r.returncode == 0 and '5/5 fixtures' in r.stdout
r = subprocess.run([sys.executable, str(test), '--emit-dir', str(scratch/'capture')], env=env, capture_output=True, text=True)
assert r.returncode == 0, r.stderr
(packet / 'fixture-generation.log').write_text(r.stdout)
print(json.dumps(results))
print('PASS: series apply/reapply/reverse/reapply; patch reconstruction and all five omissions; fixture emission')
