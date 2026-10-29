#!/usr/bin/env python3
"""Audit published receipt bytes, mutation outcomes, and untouched source."""
import ast, hashlib, json, os, pathlib, re, subprocess, sys
P=pathlib.Path(__file__).resolve().parent
S=pathlib.Path(sys.argv[1]).resolve()
manifest={x['file']:x for x in json.loads((P/'published-manifest.json').read_text())}
n=0
for f in sorted((P/'public').rglob('*')):
    if not f.is_file(): continue
    rel=f.relative_to(P/'public').as_posix()
    got=hashlib.sha256(f.read_bytes()).hexdigest()
    assert got==manifest[rel]['published_sha256'], ('digest mismatch',rel,got)
    n+=1
print('Published receipt SHA-256 matches:',n)
module=ast.parse((S/'tb/pp_top/aecp_dispatch_mutants.py').read_text())
arms=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MUTANTS' for t in n.targets))
readme=(S/'tb/pp_top/README.md').read_text()
logs=P/'public/author-r2/receipts/campaigns/aecp-dispatch-ec1ff27/out'
results=[]
for name,patch,target,expected in arms:
    if not name.startswith('rbt-'): continue
    subprocess.run(['git','apply','--check',str(S/'tb/pp_top/aecp_dispatch_mutations'/(patch+'.patch'))],cwd=S,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    body=(logs/(name+'.log')).read_text()
    failures=[line for line in body.splitlines() if line.startswith('FAIL:')]
    named=[line for line in failures if line[5:].strip().startswith(expected)]
    row=next(x for x in readme.splitlines() if x.startswith('| `'+name+'`'))
    count=int(row.split('|')[-2].strip())
    assert '[build default,' in body and named and len(failures)==count,(name,len(failures),count,named)
    results.append({'arm':name,'verdict':'KILLED','failures':len(failures),'named':len(named),'expected':expected})
    print(name, 'KILLED', 'failures='+str(len(failures)), 'named='+str(len(named)))
assert len(results)==30
print('All 30 REBOOT patches apply to the exact head without edits.')
(P/'mutation-audit.json').write_text(json.dumps(results,indent=2)+'\n')
for f in sorted((P/'public/author-r2/receipts').rglob('*.rc')):
    print(f.relative_to(P/'public'), 'rc='+f.read_text().strip())
    assert f.read_text().strip()=='0'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip()
tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=S,text=True).strip()
assert head=='ec1ff275a72d885f0908fd213d8009e9e4dda4d9'
assert tree=='be6818cf5ccccf5d327cc43adaec34c1df51b98c'
index=subprocess.check_output(['git','ls-files','--stage','-z'],cwd=S).split(b'\0')
expected=subprocess.check_output(['git','ls-tree','-rz','HEAD'],cwd=S).split(b'\0')
tree_map={}
for ent in expected:
    if ent:
        meta,path=ent.split(b'\t'); mode,kind,sha=meta.split();tree_map[path]=(mode,sha)
blobs=0;links=[]
for ent in index:
    if not ent:continue
    meta,path=ent.split(b'\t');mode,sha,stage=meta.split()
    assert stage==b'0' and tree_map.pop(path)==(mode,sha)
    if mode==b'160000':links.append(os.fsdecode(path));continue
    f=S/os.fsdecode(path)
    data=os.fsencode(os.readlink(f)) if mode==b'120000' else f.read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
    assert got==sha, path
    if mode!=b'120000': assert bool(f.stat().st_mode & 0o111)==(mode==b'100755'),path
    blobs+=1
assert not tree_map
print('Tracked blobs/modes/index exact:',blobs)
print('Submodule gitlinks:',links)
print('HEAD:',head,'tree:',tree)
print('Source status:',subprocess.check_output(['git','status','--porcelain'],cwd=S,text=True).strip() or 'clean')
