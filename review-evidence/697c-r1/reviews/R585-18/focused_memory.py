#!/usr/bin/env python3
"""Independently exercise the new capture and its dependency verdict."""
import ast
from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
packet = Path(__file__).resolve().parent
work = packet / 'scratch/focused-memory'
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_boundary as boundary
import ctrl_capture as recorder
import ctrl_configs as configs
from ctrl_build import Refusal

builder = 'sw/litex/test_ctrl_memory.py'
capture_dir = work / 'capture'
result = recorder.run(capture_dir, [sys.executable, builder, '--build-only'], cwd=root,
                      capture_output=True, text=True)
print('clean build', result.returncode, result.stdout, result.stderr)
assert result.returncode == 0
capture = recorder.load(capture_dir)
reset = [s for i in capture.invocations for s in i.sources if s.path.endswith('/ctrl_split_start.S')]
assert len(reset) == 1 and reset[0].deps is not None
assert builder in capture.ran
print('reset source', reset[0].path, 'language', reset[0].lang, 'dependencies', reset[0].deps.files)
places = boundary.Places((root,), boundary.targets(capture, (root,)))
assert not boundary.judged(capture, places)
print('clean reset entry: no boundary finding')

# Ask the complete census for each diagnostic. Missing unrelated captures are
# expected in this focused run; require the new builder diagnostic specifically.
scope = configs.Scope(frozenset({'verilator'}))
try:
    configs.held(capture, scope)
except Refusal as exc:
    assert f'no invocation of {builder} from a run of its own' not in str(exc)
    print('present fifth capture: its missing-run diagnostic is absent')
empty = replace(capture, invocations=(), parts=())
try:
    configs.held(empty, scope)
except Refusal as exc:
    needle = f'the capture holds no invocation of {builder} from a run of its own'
    assert needle in str(exc)
    print('dropped fifth capture:', needle)
else:
    raise AssertionError('dropped fifth capture accepted')

for name in ('test_ctrl_memory.py', 'ctrl_memory.py', 'milan_soc.py'):
    planted = root / 'sw/firmware/ctrl/test' / ('independent_' + name)
    try:
        configs.held(capture, scope, {planted: (root / 'sw/litex' / name).read_text()})
    except Refusal as exc:
        needle = str(planted.relative_to(root)) + " names the firmware's tree and is a program"
        assert needle in str(exc)
        print('unclassified copy:', needle)
    else:
        raise AssertionError('unclassified copy accepted')

# Replay the actual assembler invocation against a disposable layout. Preserve
# compiler flags; inject a private header which preprocesses to no instructions.
inv = next(i for i in capture.invocations if any(s.path.endswith('/ctrl_split_start.S') for s in i.sources))
copy = work / 'copy'
src = copy / 'sw/firmware/ctrl/plat/ctrl_split_start.S'
private = copy / 'third_party/tsn-c-stack/examples/port/boundary_private.h'
private.parent.mkdir(parents=True, exist_ok=True)
private.write_text('/* boundary probe: private header, deliberately empty */\n')
src.parent.mkdir(parents=True, exist_ok=True)
src.write_text('#include "' + str(private) + '"\n' + Path(reset[0].path).read_text())
args = list(inv.args)
args = [str(src) if a == reset[0].path else a for a in args]
args[args.index('-o') + 1] = str(work / 'planted.o')
planted_dir = work / 'planted-capture'
r = recorder.run(planted_dir, [inv.tool, *args], cwd=root, capture_output=True, text=True)
assert r.returncode == 0, r.stderr
planted_capture = recorder.load(planted_dir)
places = boundary.Places((copy, root), boundary.targets(planted_capture, (copy, root)))
findings = boundary.judged(planted_capture, places)
assert any('ctrl_split_start.S reads tsn-c-stack/examples/port/boundary_private.h' in f for f in findings)
for f in findings: print('private include:', f)

r = subprocess.run([sys.executable, builder, '--build-only'], capture_output=True, text=True,
                   env=dict(os.environ, MILAN_RV32_CC=str(work / 'no-such-compiler')))
assert r.returncode == 2 and 'reset-entry build needs an RV32 compiler' in r.stderr
print('missing RV32 compiler: named refusal, rc 2')

old = ast.parse(subprocess.check_output(['git', 'show', 'd5858bbe:sw/litex/test_ctrl_memory.py'], text=True))
new = ast.parse((root / 'sw/litex/ctrl_memory_probe.py').read_text())
for name in ('link', 'PROBE'):
    def selected(tree):
        return next(n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name == name) or
                    (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)))
    assert ast.dump(selected(old)) == ast.dump(selected(new))
    print(name, 'AST identical to dev')
print('focused memory capture: PASS')
