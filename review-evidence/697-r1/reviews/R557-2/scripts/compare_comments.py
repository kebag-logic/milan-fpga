#!/usr/bin/env python3
"""Compare the comment-reduction boundary using actual CI compile commands."""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tarfile

repo, packet = map(lambda s: Path(s).resolve(),sys.argv[1:3])
before='086e5d37c19fbb6f4a628c376ce8f9f20e51df14'
after='ccb4ac30b03682d68a52fe7f1eb375b0c8bfb9d3'
root=packet/'scratch/comment-compare'
source=root/'source'
root.mkdir(parents=True,exist_ok=True)
source.mkdir(exist_ok=True)
out=packet/'receipts/comment-comparison'
out.mkdir(parents=True,exist_ok=True)
def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
def blob(ref,path):return git('show',ref+':'+path).decode()
token=re.compile(r'R"([^ ()\\\t\r\n]*)\(.*?\)\1"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/|[A-Za-z_]\w*|(?:\d+\.?\w*|\.\d+)\w*|>>=|<<=|\.\.\.|->|\+\+|--|&&|\|\||<<|>>|<=|>=|==|!=|[+*/%&|^!-]=|##|[^\s]',re.S)
def tokens(s):return [m[0] for m in token.finditer(s) if not m[0].startswith(('//','/*'))]
files=[p for p in git('ls-tree','-r','--name-only',after).decode().splitlines()
       if p.split('/')[0] in ('src','include','tests','examples') and Path(p).suffix in ('.c','.h','.cpp','.hpp','.S','.ld')]
file_results=[]
for p in files:
    a,b=tokens(blob(before,p)),tokens(blob(after,p))
    file_results.append({'path':p,'equal':a==b,'tokens':len(a)})
assert all(x['equal'] for x in file_results)
old,new=(json.loads(blob(r,'tests/mutations.json')) for r in (before,after))
assert [m['name'] for m in old]==[m['name'] for m in new]
plants=[]
for a,b in zip(old,new):
    assert a['path']==b['path'] and a['kills']==b['kills']
    x,y=(blob(r,m['path']) for r,m in ((before,a),(after,b)))
    assert x.count(a['old'])==y.count(b['old'])==1
    equal=tokens(x.replace(a['old'],a['new']))==tokens(y.replace(b['old'],b['new']))
    assert equal,a['name']
    plants.append({'name':a['name'],'program_tokens_equal':equal,'killers_equal':True})

commands=[]
for variant in ('gcc','clang-sanitizers','rv32/debug','rv32/release'):
    build=packet/'scratch/runs'/variant
    for entry in json.loads((build/'compile_commands.json').read_text()):
        if Path(entry['file']).parent!=repo/'src':continue
        args=shlex.split(entry['command'])
        mapped=[a.replace(str(repo),str(source)).replace(str(build),str(root/'build'/variant)) for a in args]
        mapped+=['-g0','-frandom-seed=0']
        cwd=root/'build'/variant
        cwd.mkdir(parents=True,exist_ok=True)
        obj=cwd/mapped[mapped.index('-o')+1]
        obj.parent.mkdir(parents=True,exist_ok=True)
        commands.append((variant,mapped,cwd,obj))
assert len(commands)==22,len(commands)
hashes={}
for ref in (before,after):
    with tarfile.open(fileobj=io.BytesIO(git('archive',ref))) as archive:
        archive.extractall(source,filter='data')
    hashes[ref]=[]
    for variant,argv,cwd,obj in commands:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert p.returncode==0,p.stdout
        hashes[ref].append(hashlib.sha256(obj.read_bytes()).hexdigest())
assert hashes[before]==hashes[after]
objects=[]
for i,(variant,argv,cwd,obj) in enumerate(commands):
    label=str(obj.relative_to(root/'build'))
    objects.append({'object':label,'before_sha256':hashes[before][i],'after_sha256':hashes[after][i],
        'equal':True,'command':' '.join(argv).replace(str(root),'<COMPARE>')})
results={'before':before,'after':after,'code_files':file_results,'mutants':plants,'objects':objects}
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(f'{len(files)} code files retain non-comment tokens; {len(plants)} mutant programs and killer mappings match; {len(objects)}/22 core objects byte-identical.')
