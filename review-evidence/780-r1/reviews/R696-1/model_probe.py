#!/usr/bin/env python3
"""Reproduce the existing served-inventory model's GET_AVB_INFO input.

Run from the parent checkout. No source changes are made.
"""
import ast
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path('tests/steps').resolve()))
import aecp_engine_model as m

# Read the actual inventory expression without importing the step framework.
tree=ast.parse(Path('tests/steps/aecp_engine_steps.py').read_text())
assignment=next(n for n in tree.body if isinstance(n,ast.Assign)
                and any(isinstance(t,ast.Name) and t.id=='SERVED' for t in n.targets))
node=next(v for k,v in zip(assignment.value.keys,assignment.value.values)
          if isinstance(k,ast.Constant) and k.value==0x27)
row=eval(compile(ast.Expression(node),'<served-row>','eval'),
         {'dict':dict,'ST_SUCCESS':m.ST_SUCCESS})
print('Inventory row:',row)
command=m.build_aem_command(0x27)
payload=m.decode_command(command)['payload']
model=m.AecpEngineModel({0x27:row},m.DescriptorImage(),mvu_served={})
status=m.decode(model.deliver(command))['status']
print('Default sweep command payload:',payload.hex())
print('GET_AVB_INFO descriptor_type:',int.from_bytes(payload[:2],'big'))
print('Model response status:',status)
assert payload==bytes(8) and status==0
print('Confirmed: generic ENTITY[0] operands and SUCCESS inventory row, not an AVB_INTERFACE-only query.')
print('No NOT_IMPLEMENTED/status-1 expectation for this case; this model does not prove wrong-target wire behavior.')
