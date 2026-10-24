#!/usr/bin/env python3
"""Reproduce the existing GET_AVB_INFO inventory-model observation."""
import ast
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
path = root / 'tests/steps/aecp_engine_model.py'
spec = importlib.util.spec_from_file_location('aecp_model_probe', path)
model = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = model
spec.loader.exec_module(model)
tree = ast.parse((root / 'tests/steps/aecp_engine_steps.py').read_text())
assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'SERVED' for t in n.targets))
served = eval(compile(ast.Expression(assignment.value), '<inventory>', 'eval'), vars(model))
command = model.build_aem_command(0x0027)
mvu_assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == 'SERVED_MVU' for t in n.targets))
mvu = eval(compile(ast.Expression(mvu_assignment.value), '<mvu-inventory>', 'eval'), vars(model))
response = model.AecpEngineModel(served, model.DescriptorImage(), mvu_served=mvu).deliver(command)
result = {'opcode': 39, 'descriptor_type': int.from_bytes(command[38:40], 'big'),
          'descriptor_index': int.from_bytes(command[40:42], 'big'),
          'status': model.decode(response)['status'], 'inventory_status': served[39]['verdict']}
print(json.dumps(result, sort_keys=True))
assert result['descriptor_type'] == 0 and result['descriptor_index'] == 0
assert result['status'] == result['inventory_status'] == 0
print('PASS: existing inventory model returns SUCCESS for generic ENTITY[0]; no wire-status proof')
