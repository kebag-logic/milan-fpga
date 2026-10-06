#!/usr/bin/env python3
"""Plant every checked-in patch independently and both exact-edit tables.

Usage: python3 check_planting.py SOURCE PACKET
No source checkout is changed; all mutations are disposable.
"""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
source,packet = map(Path,sys.argv[1:])
tree=packet/'scratch'/'planting'
tree.mkdir(parents=True,exist_ok=True)
for directory in ('hdl','tb'):
    shutil.copytree(source/directory,tree/directory,dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('obj*','__pycache__'))
receipts=[]
for patch in sorted((source/'tb').rglob('*.patch')):
    # All patches operate on tracked files; restore scratch bytes between trials.
    touched=set()
    for line in patch.read_text().splitlines():
        if line.startswith('+++ b/'): touched.add(line[6:].split('\t')[0])
    saved={name:(tree/name).read_bytes() for name in touched}
    r=subprocess.run(['git','apply','--check',str(patch)],cwd=tree,capture_output=True,text=True)
    if r.returncode==0:
        r=subprocess.run(['git','apply',str(patch)],cwd=tree,capture_output=True,text=True)
    receipts.append({'patch':str(patch.relative_to(source)),'rc':r.returncode,'detail':r.stderr})
    for name,body in saved.items(): (tree/name).write_bytes(body)
for name in ('d3_mutants','notify_mutants'):
    spec=importlib.util.spec_from_file_location(name,source/'tb/pp_top'/f'{name}.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for m in module.MUTANTS:
        saved={rel:(tree/rel).read_bytes() for rel,_,_ in m.edits}
        reason=module.plant(tree,m.edits)
        receipts.append({'table':name,'mutant':m.name,'rc':int(bool(reason)),'detail':reason})
        for rel,body in saved.items(): (tree/rel).write_bytes(body)
out=packet/'receipts/planting.json'
out.write_text(json.dumps(receipts,indent=2)+'\n')
for r in receipts:
    if r['rc']: print(json.dumps(r))
print(f'PLANTING {len(receipts)} trials, {sum(r["rc"] != 0 for r in receipts)} failures')
raise SystemExit(any(r['rc'] for r in receipts))
