"""Partition independent fixture tables of the unchanged profile gate.

All setup, reason controls and non-table assertions run in each partition.
Completion requires every partition and an exact union of every selected table.
The candidate source is read, never modified. Original aggregate prose describes
the complete table; the receipt below records what this invocation actually ran.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import time

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--root', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--part', type=int, required=True)
p.add_argument('--parts', type=int, required=True)
p.add_argument('--absent', action='store_true')
a = p.parse_args()
assert 0 <= a.part < a.parts
a.root = a.root.resolve()
a.output.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(a.root / 'sw/builder'))
sys.argv = [sys.argv[0], '--require-rv32']
import test_builder as bank

source = a.root / 'sw/builder/test_builder.py'
tree = ast.parse(source.read_text())
function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == 'test_baremetal_profile_contract')
sites = [n for n in function.body if isinstance(n, ast.For)
         and isinstance(n.target, ast.Name) and n.target.id == 'mutation'
         and isinstance(n.iter, ast.Name) and n.iter.id == 'mutations']
assert len(sites) == 1 and len(sites[0].body) == 1
assert ast.unparse(sites[0].body[0]) == 'assert_rejected(*mutation)'
receipt = {'part': a.part, 'parts': a.parts,
           'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}

def selected(tag, iterable):
    """Record the entire original table, then yield a disjoint positional slice."""
    table = list(iterable)
    names = [row[0] for row in table]
    assert len(names) == len(set(names))
    record = {'table': names, 'selected': names[a.part::a.parts]}
    receipt.setdefault('tables', {})[tag] = record
    (a.output / 'started.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('PROFILE PARTITION', tag, a.part, 'OF', a.parts, 'SELECTED', len(record['selected']),
          'OF', len(names), flush=True)
    for row in table[a.part::a.parts]:
        print('PROFILE FIXTURE', tag, row[0], flush=True)
        yield row

chosen = {'mutations': sites[0]}
for node in ast.walk(function):
    if not isinstance(node, ast.For):
        continue
    spelling = ast.unparse(node.iter)
    if spelling in ('accepted_cases.items()', 'accepted_makefiles.items()'):
        assert spelling not in chosen
        chosen[spelling] = node
    if spelling == 'controls.items()' and 17050 < node.lineno < 17102:
        chosen['disconnected identity controls'] = node
assert len(chosen) == 4, chosen.keys()
for tag, node in chosen.items():
    node.iter = ast.Call(func=ast.Name(id='f5_profile_selected', ctx=ast.Load()),
                         args=[ast.Constant(tag), node.iter], keywords=[])
unit = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
bank.__dict__['f5_profile_selected'] = selected
exec(compile(unit, str(source), 'exec'), bank.__dict__)
start = time.monotonic()
if a.absent:
    import test_firmware_compiler
    test_firmware_compiler.run_gate(None, a.output / 'compiler-audit.jsonl', False)
else:
    bank.test_baremetal_profile_contract()
receipt.update(rc=0, seconds=time.monotonic()-start, nonexecuted=bank.SKIPPED)
(a.output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PROFILE PARTITION PASS', a.part, flush=True)
