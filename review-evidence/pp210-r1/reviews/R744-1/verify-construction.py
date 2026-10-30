#!/usr/bin/env python3
"""Compare build inputs and regenerate both shipped ROMs at base and head."""
import hashlib,os,pathlib,re,subprocess,sys,tempfile
src=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve()
base='a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645'; head='18a4dc1fcf91528a52737d5ea830b5acd5d543c4'
def git(*a): return subprocess.check_output(['git','-C',str(src),*a])
changed=git('diff','--name-only',base,head).decode().splitlines()
other=[x for x in changed if not x.endswith('.md')]
assert set(other)=={'Makefile','scripts/check-doc-inventory.py','scripts/check-links.py'},other
print('Changed files:',len(changed));print('Non-Markdown delta:',other)
print('All other tracked paths and modes, including RTL, generators, models, build recipes, workflow and committed outputs: IDENTICAL')
print(git('diff',base,head,'--','Makefile').decode())
print('Top Makefile: added read-only inventory target and check prerequisite only; no ROM/build/render recipe changed.')
print('Submodule gitlinks:',git('ls-tree','-r',head).decode().count('160000 commit '),'(none)')
results={}
for label,rev in [('base',base),('head',head)]:
 root=pathlib.Path(tempfile.mkdtemp(prefix='generated-'+label+'-',dir=out/'scratch'))/'tree'
 subprocess.run(['git','clone','-q','--shared','--no-checkout',str(src),str(root)],check=True)
 subprocess.run(['git','-C',str(root),'checkout','-q','--detach',rev],check=True)
 results[label]={}
 for name,script in [('ucode','hdl/aecp/ucode/gen_ucode.py'),('listener','hdl/acmp/rom/gen_ltn_rom.py')]:
  dest=root/(name+'.hex')
  r=subprocess.run(['python3','-B',script,'-o',str(dest)],cwd=root,capture_output=True,text=True,check=True)
  data=dest.read_bytes(); results[label][name]=hashlib.sha256(data).hexdigest()
  print(label,name,'lines',len(data.splitlines()),'sha256',results[label][name])
  if name=='ucode':
   words=[int(x,16) for x in data.decode().splitlines()]
   shifts=[i for i,w in enumerate(words) if (w>>43)==29]
   print(label,'generated SHIFT_R opcode=29 count',len(shifts),'addresses',shifts)
assert results['base']==results['head']
print('Generated ROM outputs: BYTE IDENTICAL')
# Full bytes/modes/index check of the untouched review checkout.
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()=='7cdbc61bb2296f923585b42d3cd0a01baf6d3991'
assert git('write-tree').decode().strip()=='7cdbc61bb2296f923585b42d3cd0a01baf6d3991'
count=0
for record in git('ls-files','--stage','-z').split(b'\0'):
 if not record: continue
 meta,path=record.split(b'\t',1);mode,blob,stage=meta.split();name=os.fsdecode(path);f=src/name
 assert stage==b'0' and mode!=b'160000'
 data=f.read_bytes(); actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
 assert actual==blob,name
 assert bool(f.stat().st_mode&0o111)==(mode==b'100755'),name
 count+=1
assert not git('status','--porcelain')
print('Original checkout verified:',count,'tracked blob bytes and executable modes, exact index tree, clean worktree.')
