#!/usr/bin/env python3
import pathlib,subprocess,json,re,hashlib
p=pathlib.Path(__file__).resolve().parents[1]; root=p/'scratch/tree'
def git(*a): return subprocess.check_output(['git','-C',str(root),*a],text=True).strip()
head='80588cdc43ca5605a1d3748d13dd8ed7f22f7000'; base='c050d97153dd0480ae741102c1647eeda9b7f273'
assert git('rev-parse','HEAD')==head
results=[]
for rev in ['07b1469d','b0a74196','ead80360','5b2199b','e219709',head]:
 parents=git('rev-list','--parents','-n1',rev).split()
 assert len(parents)==3
 r=subprocess.run(['git','-C',str(root),'merge-tree','--write-tree',*parents[1:]],capture_output=True,text=True)
 expected=git('rev-parse',rev+'^{tree}')
 results.append(dict(commit=parents[0],parents=parents[1:],rc=r.returncode,expected_tree=expected,computed=r.stdout.strip(),stderr=r.stderr))
 assert r.returncode==0 and r.stdout.strip()==expected
print('Clean merge-tree reconstructions:',json.dumps(results,indent=2))
def scanned(rev):return set(git('ls-tree','-r','--name-only',rev,'--','docs','hdl','tb').splitlines())
a=scanned('91cef52'); b=scanned(head)
added=sorted(b-a); removed=sorted(a-b)
merged_added=set()
for rev in ['5b2199b','e219709',head]: merged_added |= scanned(rev)-scanned(rev+'^1')
assert len(a)==488 and len(b)==531 and len(added)==43 and not removed and set(added)==merged_added
assert not (scanned('3d5a201')-a)
print('Scan file inventory:',json.dumps(dict(before=len(a),after=len(b),added=added,removed=removed,exactly_merge_added=True),indent=2))
# The C11 delta against landed main has only comment changes in RTL and C++.
paths=git('diff','--name-only','ead80360',head,'--','hdl','tb').splitlines()
for name in paths:
 if name.endswith(('.sv','.cpp','.hpp')):
  def norm(ref):
   s=git('show',ref+':'+name)
   s=re.sub(r'/\*.*?\*/','',s,flags=re.S); s=re.sub(r'//[^\n]*','',s)
   return re.sub(r'\s+','',s)
  assert norm('ead80360')==norm(head),name
print('C11 hdl/tb delta against landed main:',json.dumps(paths));print('Executable-token comparison PASS')
print('Source history:',git('log','--first-parent','--format=%H %P %s',base+'..'+head))
print('Gitlinks at source head:',git('ls-tree','-r',head) if False else [x for x in git('ls-tree','-r',head).splitlines() if x.startswith('160000')])
