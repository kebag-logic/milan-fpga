#!/usr/bin/env python3
"""Compare the changed plan section against its prior implementation on every config."""
import ast
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path('sw/builder').resolve()))
import endstation_builder as builder

old = subprocess.check_output(['git', 'show', '64d539f1:sw/builder/endstation_builder.py'], text=True)
node = next(n for n in ast.parse(old).body if isinstance(n, ast.FunctionDef) and n.name == '_plan_ports')
namespace = dict(builder.__dict__)
exec(compile(ast.Module(body=[node], type_ignores=[]), '<prior-plan-function>', 'exec'), namespace)
count = 0
for p in sorted(Path('configs').glob('endstation_*.yaml')):
    cfg = builder.load_config(str(p))
    before = '\n'.join(namespace['_plan_ports'](cfg))
    after = '\n'.join(builder._plan_ports(cfg))
    unrouted = any(g['role'] == 'unrouted' for port in cfg['ports_in'] for g in port['pool'])
    expected = before.replace('`Loopback S<s> ch <c>` - so a ', '`Loopback S<s> ch <c>`, `Unrouted S<p>` - so a ') if unrouted else before
    assert after == expected, p
    print(f'{p.name}: unrouted={unrouted}; plan delta={len(after)-len(before)} bytes; PASS')
    count += 1
assert count == 5, count
print('5/5 tracked configurations: only the unrouted-name example changes')
