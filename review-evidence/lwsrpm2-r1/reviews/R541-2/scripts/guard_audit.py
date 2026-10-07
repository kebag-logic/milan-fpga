# SPDX-License-Identifier: Apache-2.0
"""Cross-check changed guard bodies against compiler statement nodes."""
from pathlib import Path
import argparse
import json
import re
import subprocess
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
a=p.parse_args();root=a.source.resolve();packet=a.packet.resolve()
results=[]
for file in ['src/core/mrp_mad.c','src/core/mrp_pdu.c','src/modules/msrp.c',
             'src/modules/mmrp.c','src/modules/mvrp.c','tests/unit/review_test.c']:
    text=(root/file).read_bytes().decode('latin1')
    diff=subprocess.check_output(['git','diff','-U0',
        '1401654530ce7d9275de9b901e67df47e5bbc536..HEAD','--',file],cwd=root,text=True)
    changed=set()
    for m in re.finditer(r'^@@ .*?\+(\d+)(?:,(\d+))? @@',diff,re.M):
        start=int(m[1]);changed.update(range(start,start+int(m[2] or 1)))
    cmd=['clang','-std=c11','-Isrc/include','-Isrc','-I'+str(packet/'scratch/deps/include'),
         '-Xclang','-ast-dump=json','-fsyntax-only',file]
    r=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
    assert r.returncode==0,r.stderr
    checked=[];bad=[]
    def visit(n):
        if n.get('kind') in ['IfStmt','ForStmt','WhileStmt','DoStmt']:
            start=n.get('range',{}).get('begin',{}).get('offset',-1)
            inner=n.get('inner',[])
            if 0<=start<len(text) and text[start:].startswith(('if','for','while','do')) and inner:
                bodies=inner[-2:] if n.get('hasElse') else inner[-1:]
                for body in bodies:
                    pos=body.get('range',{}).get('begin',{}).get('offset',start)
                    left=text[:start].count('\n')+1;right=text[:pos].count('\n')+1
                    if changed.intersection(range(left,right+1)):
                        checked.append(left)
                        if body['kind'] not in ['CompoundStmt','IfStmt']:
                            bad.append((left,body['kind']))
        for child in n.get('inner',[]):visit(child)
    visit(json.loads(r.stdout))
    results.append(f'{file}: changed guards examined={len(checked)}; lines={checked}; unbraced={bad}')
out='\n'.join(results)+'\n'
(packet/'receipts/guard-audit.txt').write_text(out)
print(out)
