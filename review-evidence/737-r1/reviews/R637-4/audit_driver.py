#!/usr/bin/env python3
"""Prove gate bytes unchanged; exercise entry points with inert call-recording gates."""
import ast, contextlib, io, json, pathlib, subprocess, sys, typing, types
from unittest.mock import patch
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(__file__).resolve().parent
path='sw/builder/test_builder.py'
old=subprocess.check_output(['git','show','84ee9ea1:'+path],cwd=root,text=True);new=(root/path).read_text()
a,b=ast.parse(old),ast.parse(new)
def functions(t,s):
 lines=s.splitlines(keepends=True)
 return {n.name:''.join(lines[n.lineno-1:n.end_lineno]) for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
assert functions(a,old)==functions(b,new)
assert ast.dump(ast.Module(body=a.body[1:-1],type_ignores=[]))==ast.dump(ast.Module(body=b.body[1:-1],type_ignores=[]))
loop=lambda t:next(n for n in t.body[-1].body if isinstance(n,ast.For))
names=[n.id for n in loop(a).iter.elts]
assert [n.id for n in loop(b).iter.args[1].elts]==names and len(names)==103
verdict=next(n for n in b.body if isinstance(n,ast.FunctionDef) and n.name=='_require_elaboration_verdict')

def invoke(tree,args,fail=None):
 called=[]; ledger=[]
 def gate(name):
  def run():
   called.append(name)
   if name==fail:raise AssertionError('planted gate failure')
   if name in ('test_baremetal_profile_contract','test_resource_calibration'):
    ledger.append((name,'synthetic unavailable row','row'))
  run.__name__=name;return run
 env={'__name__':'__main__','sys':sys,'json':json,'Callable':typing.Callable,'SKIPPED':ledger,'NO_LITEX':'no-litex','TOOLCHAIN':'toolchain'}
 env.update({name:gate(name) for name in names})
 exec(compile(ast.Module(body=[verdict],type_ignores=[]),path,'exec'),env)
 output=io.StringIO();status=0
 modules={}
 for node in tree.body[-1].body:
  if isinstance(node,ast.ImportFrom):
   m=modules[node.module]=types.ModuleType(node.module)
   for item in node.names:setattr(m,item.name,env[item.name])
 with patch.dict(sys.modules,modules),patch.object(sys,'argv',[path,*args]),contextlib.redirect_stdout(output):
  try:exec(compile(ast.Module(body=[tree.body[-1]],type_ignores=[]),path,'exec'),env)
  except SystemExit as e:status=e.code or 0
  except AssertionError as e: status=str(e)
 return called,ledger,output.getvalue(),status
results={}
for args in ([],['--require-elaboration'],['--require-elaboration','--require-rv32']):
 x,y=invoke(a,args),invoke(b,args);assert x==y
 assert x[0]==names and 'SUBSET' not in x[2];results[str(args)]='identical baseline/default execution order, ledger, stdout, status (instrumented gates)'
assert json.loads(invoke(b,['--list'])[2])==names
for selection in ['unknown',names[0]+','+names[0],names[1]+','+names[0],'']:
 x=invoke(b,['--gates',selection]);assert not x[0] and x[3]
x=invoke(b,['--gates']);assert not x[0] and x[3]
receipt=out/'scratch'/'driver-probe.json';receipt.unlink(missing_ok=True)
x=invoke(b,['--gates',names[0]+','+names[2],'--receipt',str(receipt)])
r=json.loads(receipt.read_text());assert x[0]==[names[0],names[2]] and r['selected']==x[0] and [g['gate'] for g in r['gates']]==x[0]
receipt.unlink();x=invoke(b,['--gates',names[0],'--receipt',str(receipt)],fail=names[0]);assert not receipt.exists() and x[3]=='planted gate failure'
result={'gate_function_bytes_unchanged':len(functions(b,new)),'all_pre_entrypoint_code_ast_unchanged':True,'inventory_count':len(names),'ordered_inventory_unchanged':True,'default_entrypoint_controls':results,'invalid_selection_controls':5,'subset_receipt_control':'PASS','failed_gate_no_receipt':'PASS','limit':'Entry-point controls use inert call-recording gate functions; they do not execute the full builder bank.'}
(out/'driver-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
