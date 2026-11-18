#!/usr/bin/env python3
"""Compare relocated mutation ASTs without importing candidate modules."""
import ast, subprocess
def tree(rev,path): return ast.parse(subprocess.check_output(['git','show',f'{rev}:{path}'],text=True))
def assigned(t,name):
    for n in t.body:
        if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id==name:return n.value
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):return n.value
    raise ValueError(name)
def dump(n):return ast.dump(n,include_attributes=False)
base='tb/verilator/ctrl_service_budget/'
for commit,module in [('7431b6ba','selftest_mutants_burst'),('4a5bfb32','selftest_mutants_mrp')]:
    before=assigned(tree(commit+'^',base+'selftest_mutants.py'),'MUTANTS')
    after=assigned(tree(commit,base+'selftest_mutants.py'),'MUTANTS')
    moved=assigned(tree(commit,base+module+'.py'),'MUTANTS')
    keys=[];values=[]
    for k,v in zip(after.keys,after.values):
        if k is None and isinstance(v,ast.Attribute) and isinstance(v.value,ast.Name) and v.value.id==module:
            keys+=moved.keys;values+=moved.values
        else:keys.append(k);values.append(v)
    after.keys=keys;after.values=values
    assert dump(before)==dump(after),commit
    print('PASS',commit,'ordered mutation dictionary AST equal after in-place expansion',len(keys),'entries')
commit='b1af3b54';path='sw/firmware/ctrl/test/aecp_mutants.py'
before=assigned(tree(commit+'^',path),'DEFECTS');after=assigned(tree(commit,path),'DEFECTS')
while isinstance(before,ast.BinOp):before=before.left
while isinstance(after,ast.BinOp):after=after.left
rows=assigned(tree(commit,'sw/firmware/ctrl/test/aecp_stream_info_mutants.py'),'ROWS')
expanded=[]
for e in after.elts:
    if isinstance(e,ast.Starred) and isinstance(e.value,ast.GeneratorExp):
        expanded.extend(ast.Call(func=ast.Name(id='defect',ctx=ast.Load()),args=r.elts,keywords=[]) for r in rows.elts)
    else:expanded.append(e)
after.elts=expanded
assert dump(before)==dump(after)
print('PASS',commit,'ordered defect tuple AST equal after in-place expansion',len(expanded),'entries')
def function(t,name):return next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name==name)
commit='afbbde54';path='sw/firmware/ctrl/test/plat_mutants.py'
b=function(tree(commit+'^',path),'phy_mutants');a=function(tree(commit,path),'phy_mutants')
m=function(tree(commit,path),'step_yield_mutants')
returned=next(n.value for n in m.body if isinstance(n,ast.Return))
class Expand(ast.NodeTransformer):
    def visit_Tuple(self,n):
        n=self.generic_visit(n);out=[]
        for e in n.elts:
            if isinstance(e,ast.Starred) and isinstance(e.value,ast.Call) and isinstance(e.value.func,ast.Name) and e.value.func.id=='step_yield_mutants':out+=returned.elts
            else:out.append(e)
        n.elts=out;return n
assert dump(b)==dump(Expand().visit(a))
print('PASS',commit,'PHY mutation function AST equal after in-place expansion')
commit='082d0037'
b=function(tree(commit+'^',base+'run.py'),'declared_verdict');a=function(tree(commit,base+'talker_notice.py'),'declared_verdict')
b.body=[n for n in b.body if not isinstance(n,ast.Import)]
class Local(ast.NodeTransformer):
    def visit_Attribute(self,n):
        if isinstance(n.value,ast.Name) and n.value.id=='talker_notice':return ast.Name(id=n.attr,ctx=n.ctx)
        return self.generic_visit(n)
assert dump(Local().visit(b))==dump(a)
print('PASS',commit,'verdict AST equal after removal of local self-import and module qualification')
