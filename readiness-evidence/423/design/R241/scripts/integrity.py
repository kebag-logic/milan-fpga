import pathlib, subprocess, json, hashlib, os, stat, sys
root=pathlib.Path('$VALIDATION_STORAGE/reviews/r241-423-design')
def git(*args):
 return subprocess.check_output(['rtk','proxy','git','--no-optional-locks','-C',str(root),*args])
paths=git('ls-files','-z','--cached','--others','--exclude-standard').split(b'\0')
entries={}
for p in sorted(set(paths)):
 if not p: continue
 rel=os.fsdecode(p); path=root/rel
 try: s=path.lstat()
 except FileNotFoundError: entries[rel]={'kind':'missing'}; continue
 kind='symlink' if stat.S_ISLNK(s.st_mode) else 'file' if stat.S_ISREG(s.st_mode) else 'dir' if stat.S_ISDIR(s.st_mode) else 'other'
 data=os.fsencode(os.readlink(path)) if kind=='symlink' else path.read_bytes() if kind=='file' else b''
 entries[rel]={'kind':kind,'mode':oct(stat.S_IMODE(s.st_mode)),'sha256':hashlib.sha256(data).hexdigest()}
idx=pathlib.Path(os.fsdecode(git('rev-parse','--git-path','index')).strip())
if not idx.is_absolute(): idx=root/idx
result={'head':git('rev-parse','HEAD').decode().strip(),'index_sha256':hashlib.sha256(idx.read_bytes()).hexdigest(),'index_entries':git('ls-files','--stage').decode(),'status':git('status','--porcelain=v1','--untracked-files=all').decode(),'files':entries}
pathlib.Path(sys.argv[1]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({'head':result['head'],'status':result['status'],'entries':len(entries),'index_sha256':result['index_sha256']}))
