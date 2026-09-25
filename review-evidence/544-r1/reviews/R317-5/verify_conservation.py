#!/usr/bin/env python3
"""Compare corpus declarations and production bytes without executing payloads."""
import ast,hashlib,json,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);path='sw/builder/test_builder.py'
base='ffcbd33de70278ae34b533dcbadde0b36c8cba13';r2='77e9ca5ea9e04a7618c577ab511baec63b39dc05'
def read(rev,path):return subprocess.check_output(['git','-C',str(root),'show',rev+':'+path])
def declarations(rev):
    source=read(rev,path).decode();tree=ast.parse(source)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='test_baremetal_profile_contract')
    rows=[]
    for n in fn.body:
        names=[]
        if isinstance(n,(ast.Assign,ast.AugAssign)):
            targets=n.targets if isinstance(n,ast.Assign) else [n.target]
            names=[x.id for x in targets if isinstance(x,ast.Name)]
        if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name):names=[n.value.func.value.id]
        if any(x=='accepted_cases' or 'mutations' in x for x in names):rows.append((names,ast.dump(n,include_attributes=False)))
    return rows
head=declarations('HEAD');result={}
for rev in (base,r2):
    prev=declarations(rev);cursor=0
    for names,node in prev:
        while cursor<len(head) and head[cursor][1]!=node:cursor+=1
        assert cursor<len(head),(rev,names)
        cursor+=1
    result[rev]={'original_corpus_statements_retained_in_order':len(prev),'head_corpus_statements':len(head)}
for path in ('sw/firmware/milan_baremetal/milan_baremetal.c','sw/firmware/milan_baremetal/Makefile'):
    data=read('HEAD',path)
    assert data==read(base,path)==read(r2,path)
    result[path]={'unchanged':True,'sha256':hashlib.sha256(data).hexdigest()}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
