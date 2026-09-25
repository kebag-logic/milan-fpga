#!/usr/bin/env python3
"""Compare retained corpus statements and production bytes across all lane heads."""
import ast,hashlib,json,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]);output=Path(sys.argv[2])
refs=['ffcbd33de70278ae34b533dcbadde0b36c8cba13','b068763c849a18096b0f46cf9b18e0f904e4d708','77e9ca5ea9e04a7618c577ab511baec63b39dc05','8383e929fab3ff57a768c88b8b1ff9b568afcf14']
targets={'accepted_cases','accepted_makefiles','mutations','identity_bypasses','identity_absent_fixtures','identity_near_miss_fixtures','identity_escape_fixtures'}
out={};previous=[]
def show(ref,path):return subprocess.check_output(['git','-C',str(root),'show',ref+':'+path])
for ref in refs:
 tree=ast.parse(show(ref,'sw/builder/test_builder.py'));nodes=[]
 for node in ast.walk(tree):
  if isinstance(node,(ast.Assign,ast.AugAssign)):
   lhs=node.targets if isinstance(node,ast.Assign) else [node.target]
   if any(isinstance(t,ast.Name) and t.id in targets for t in lhs):nodes.append(node)
  if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call):
   f=node.value.func
   if isinstance(f,ast.Attribute) and isinstance(f.value,ast.Name) and f.value.id in targets:nodes.append(node)
 hashes=[{'line':n.lineno,'sha256':hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()} for n in sorted(nodes,key=lambda n:n.lineno)]
 sequence=[r['sha256'] for r in hashes];at=-1
 for old in previous:at=sequence.index(old,at+1)
 out[ref]=dict(statements=hashes,previous_statements_preserved_in_order=True)
 previous=sequence
for f in ['sw/firmware/milan_baremetal/milan_baremetal.c','hdl/common/csr/milan_csr.sv']:
 vals=[show(r,f) for r in refs];assert len(set(vals))==1
 out[f]=dict(unchanged_at_all_four_heads=True,sha256=hashlib.sha256(vals[0]).hexdigest())
output.write_text(json.dumps(out,indent=2)+'\n');print('PASS: retained statements unchanged and ordered; production and CSR bytes unchanged')
