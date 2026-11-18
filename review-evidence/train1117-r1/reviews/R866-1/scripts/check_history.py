#!/usr/bin/env python3
import json, subprocess, pathlib, ast
P = pathlib.Path(__file__).resolve().parents[1]
def git(*a):
    return subprocess.check_output(['git', *a])
heads = json.loads((P/'public/frozen-heads.json').read_text())
merges = ['43b954e6','877c99e4','9c0e1974','22a82038','2078c438','7c28f53f','6a8126e4','31304b74','8f6fbb84','49f005b9','3e908539']
out = P/'receipts/history'; out.mkdir(parents=True, exist_ok=True)
for item, merge in zip(heads, merges):
    parents = git('rev-list','--parents','-n','1',merge).decode().split()
    assert len(parents)==3 and parents[2]==item['head'], (item,parents)
    subprocess.run(['git','merge-base','--is-ancestor',item['head'],'HEAD'],check=True)
    rd = git('show','--format=%H%n%P%n%s','--remerge-diff',merge)
    (out/(merge+'.diff')).write_bytes(rd)
    paths = [l for l in rd.decode().splitlines() if l.startswith('diff --git')]
    print(item['pr'], item['head'], merge, 'ANCESTOR, second parent equals published head;',len(paths),'resolution files')
    print('\n'.join(paths))
for rev in ['6fef44b8','45708d9e']:
    for f in git('diff-tree','--no-commit-id','--name-only','-r',rev).decode().splitlines():
        if f.endswith('.py'):
            a=ast.dump(ast.parse(git('show',rev+'^:'+f)),include_attributes=False)
            b=ast.dump(ast.parse(git('show',rev+':'+f)),include_attributes=False)
            assert a==b,(rev,f)
            print('AST identical:',rev,f)
print('Record-only files:',git('diff-tree','--no-commit-id','--name-only','-r','HEAD').decode().strip())
assert git('diff-tree','--no-commit-id','--name-only','-r','HEAD').decode().splitlines()==['syn/ooc/pp_resource_baseline.json']
print('PASS')
