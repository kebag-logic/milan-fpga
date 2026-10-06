#!/usr/bin/env python3
"""Independent checks of the real RV32 arms and before/after object sizes."""
import ast
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch

root, packet = [Path(x).resolve() for x in sys.argv[1:3]]
work = packet / 'scratch' / 'rv32-probes'
work.mkdir()
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/ctrl_nvm/test')]
import ctrl_arms
import ctrl_build
import fw_rv32
import nvm_bench
import nvm_rv32
import test_ctrl_nvm

cc = os.environ['MILAN_RV32_CC']
BASE = '6714181d0c8a16e2983f85b724f4d688f5111835'
ctrl = work / 'ctrl'
nvm = work / 'nvm'
shutil.copytree(ctrl_build.CTRL, ctrl)
shutil.copytree(nvm_bench.TREE, nvm)
tree = ctrl_build.Tree(ctrl, work / 'ctrl-out', work / 'reuse')
cfg = root / 'configs/endstation_ax7101_1x1_tdm8.yaml'
inputs = nvm_bench.shape_inputs(cfg, work / 'inputs')
gen = work / 'gen'
nvm_bench.write_headers(gen, nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)

def ctrl_run():
    outcome = ctrl_arms.arm_rv32(tree, True)
    return outcome.rc != 0, outcome.log

def nvm_run():
    findings, sizes = nvm_rv32.build(nvm, work / 'nvm-out', gen, cc)
    return bool(findings), '\n'.join(findings)

assert not ctrl_run()[0]
assert not nvm_run()[0]
print('PASS: both real object arms build before fault injection')
for module, run, label in ((ctrl_arms, ctrl_run, 'ctrl'), (nvm_rv32, nvm_run, 'store')):
    for name, extra in [('rv32im', ('-march=rv32im',)),
                        ('ilp32d', ('-march=rv32imafd', '-mabi=ilp32d'))]:
        with patch.object(module, 'RV32_FLAGS', (*module.RV32_FLAGS, *extra)):
            failed, detail = run()
            assert failed and ('architecture attribute' in detail or 'relocatable object' in detail), detail
        print(f'PASS: real {label} arm rejects {name}')

for source, run, label in ((ctrl / 'port/shlan_port.c', ctrl_run, 'ctrl'),
                           (nvm / 'nvm_klj2.c', nvm_run, 'store')):
    original = source.read_text()
    source.write_text(original + '\nextern void consume_dynamic(char *);\n'
                      'void dynamic_probe(unsigned n) { char x[n]; consume_dynamic(x); }\n')
    failed, detail = run()
    assert failed and 'non-static stack usage' in detail, detail
    source.write_text(original)
    print(f'PASS: real {label} arm rejects compiler-reported dynamic frame')

with patch.dict(os.environ, MILAN_RV32_CC=str(work / 'absent')):
    try:
        test_ctrl_nvm.rv32_arm(inputs, work, True)
    except nvm_bench.Refusal as exc:
        assert 'no RV32 compiler' in str(exc)
    else:
        raise AssertionError('store required compiler skipped')
print('PASS: store required compiler refuses an explicit absent selector')

obj = work / 'ctrl-out/rv32/port_shlan_port.o'
obj.with_suffix('.su').unlink()
try:
    fw_rv32.stack_frames([obj])
except FileNotFoundError:
    print('PASS: missing frame file cannot pass (raises FileNotFoundError)')
else:
    raise AssertionError('missing frame file accepted')

baseline_source = subprocess.check_output(['git', '-C', str(root), 'show', BASE + ':sw/firmware/ctrl_nvm/test/nvm_rv32.py']).decode()
oldpath = work / 'baseline_nvm_rv32.py'
oldpath.write_text(baseline_source)
spec = importlib.util.spec_from_file_location('baseline_nvm_rv32', oldpath)
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
# Stack reporting is observational only; all original baseline build flags stay.
baseline.RV32_FLAGS += ('-fstack-usage',)
rows = []
for cfg in sorted((root / 'configs').glob('endstation_*.yaml')):
    shape = nvm_bench.shape_inputs(cfg, work / cfg.stem / 'inputs')
    outgen = work / cfg.stem / 'gen'
    nvm_bench.write_headers(outgen, nvm_bench.shape_header(shape.shape, shape.donor, shape.ident), shape.clock_hz)
    before_dir = work / cfg.stem / 'before'
    after_dir = work / cfg.stem / 'after'
    before_findings, before = baseline.build(nvm_bench.TREE, before_dir, outgen, cc)
    after_findings, after = nvm_rv32.build(nvm_bench.TREE, after_dir, outgen, cc)
    assert not before_findings and not after_findings
    before['stack_frame'] = fw_rv32.stack_frames(list(before_dir.glob('*.o')))
    assert after['text'] - before['text'] == -240, (cfg.stem, before, after)
    assert {k:v for k,v in before.items() if k != 'text'} == {k:v for k,v in after.items() if k != 'text'}
    def open_symbols(where):
        return subprocess.check_output([cc.removesuffix('gcc') + 'nm', '-u', *map(str, sorted(where.glob('*.o')))]).decode()
    assert '__stack_chk_fail' in open_symbols(before_dir)
    assert '__stack_chk_fail' not in open_symbols(after_dir)
    rows.append({'shape': cfg.stem, 'clock_hz': shape.clock_hz, 'before': before, 'after': after})
    print('PASS: size/stack/buffer comparison ' + json.dumps(rows[-1], sort_keys=True))

positive = ctrl_arms.arm_rv32(tree, True)
assert positive.rc == 0
assert '11520 0 170 11690' in positive.log and '112 bytes' in positive.log, positive.log
print(positive.log)
old_ctrl = subprocess.check_output(['git', '-C', str(root), 'show', BASE + ':sw/firmware/ctrl/test/ctrl_build.py']).decode()
flags = next(ast.literal_eval(node.value) for node in ast.parse(old_ctrl).body
             if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'RV32_FLAGS' for t in node.targets))
source = ctrl / 'port/ctrl_debug.c'
bad = subprocess.run([cc, *flags, *ctrl_build.includes(tree), '-c', str(source), '-o', str(work / 'baseline-ctrl.o')], capture_output=True, text=True)
assert bad.returncode != 0 and 'gnu/stubs-ilp32.h' in bad.stderr, bad.stderr
print('PASS: original ctrl command reproduces missing gnu/stubs-ilp32.h with this pinned SDK')
(packet / 'independent-sizes.json').write_text(json.dumps(rows, indent=2) + '\n')
print('Independent RV32 probes PASS')
