"""Partition only the independent plants in the unchanged saved-state self-test."""
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
a = p.parse_args()
assert 0 <= a.part < a.parts
a.root = a.root.resolve()
a.output.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(a.root / 'sw/firmware/ctrl_nvm/test'))
import test_ctrl_nvm as bank
source = a.root / 'sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py'
tree = ast.parse(source.read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'self_test')
sites = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
         and ast.unparse(n.func) == 'pool.map']
assert len(sites) == 1 and ast.unparse(sites[0].args[1]) == 'nvm_mutants.MUTANTS'
# Keep the complete listing, shape preparation and unnamed-test audit; partition
# only the work submitted to the existing pool and its unchanged plant grader.
sites[0].args[1] = ast.Subscript(value=sites[0].args[1], ctx=ast.Load(),
                                slice=ast.Slice(lower=ast.Constant(a.part), step=ast.Constant(a.parts)))
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(source), 'exec'), bank.__dict__)
start = time.monotonic()
findings = bank.self_test({}, a.output, 4)
receipt = dict(part=a.part, parts=a.parts, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
               table=[m.name for m in bank.nvm_mutants.MUTANTS],
               selected=[m.name for m in bank.nvm_mutants.MUTANTS[a.part::a.parts]],
               findings=findings, rc=int(bool(findings)), seconds=time.monotonic()-start)
(a.output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt), flush=True)
raise SystemExit(bool(findings))
