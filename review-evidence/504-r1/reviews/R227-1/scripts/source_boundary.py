import ast,json,pathlib,subprocess
ROOT=pathlib.Path('$VALIDATION_STORAGE/reviews/r227-504-r1'); OUT=pathlib.Path('$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-r1-r227'); BASE='52711029f374650dc93830d5ea28e81cb5c8f410';HEAD='3d90958f3a82ca2a9617112c107a22f332117e17'
def git(*args):return subprocess.check_output(['rtk','proxy','git','-C',str(ROOT),*args],text=True)
name='sw/builder/test_builder.py';before=ast.parse(git('show',BASE+':'+name));after=ast.parse((ROOT/name).read_text());gate=next(n for n in after.body if isinstance(n,ast.FunctionDef) and n.name=='test_baremetal_profile_contract');added=[n for n in gate.body if isinstance(n,ast.If) and n.lineno in (3975,3980)];assert len(added)==2
for n in added:gate.body.remove(n)
assert ast.dump(before,include_attributes=False)==ast.dump(after,include_attributes=False)
hosted=ast.parse((OUT/'public/hosted-source'/name).read_text());local=ast.parse((ROOT/name).read_text())
a=next(n for n in local.body if isinstance(n,ast.FunctionDef) and n.name=='test_baremetal_profile_contract');b=next(n for n in hosted.body if isinstance(n,ast.FunctionDef) and n.name==a.name);assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
print('Base-to-head builder executable AST unchanged except two requirement/logging if statements; every existing text rule, resolver residual and compiler probe unchanged. Hosted gate 1b AST exactly equals source head.')
print(git('diff','--name-status',BASE,HEAD))
