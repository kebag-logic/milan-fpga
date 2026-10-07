import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(repo,*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(repo),*args],env=env)
def check(repo,rev):
    tree=git(repo,'ls-tree','-rz',rev).split(b'\0');expected={};fail=[];links={};count=0
    for row in tree:
        if not row:continue
        info,path=row.split(b'\t',1);mode,typ,oid=info.split(); expected[path]=(mode,oid)
        f=repo/os.fsdecode(path)
        if typ==b'commit':links[os.fsdecode(path)]=oid.decode();continue
        try:
            s=f.lstat();actualmode=b'120000' if stat.S_ISLNK(s.st_mode) else (b'100755' if s.st_mode&0o111 else b'100644')
            if not (stat.S_ISLNK(s.st_mode) or stat.S_ISREG(s.st_mode)): raise ValueError('not file or link')
            data=os.fsencode(os.readlink(f)) if stat.S_ISLNK(s.st_mode) else f.read_bytes()
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
            if (actualmode,blob)!=(mode,oid): fail.append(os.fsdecode(path)+': bytes or mode')
            count+=1
        except (OSError,ValueError) as e:fail.append(os.fsdecode(path)+': '+str(e))
    indexed={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        info,path=row.split(b'\t',1);mode,oid,stage=info.split()
        if stage!=b'0' or path in indexed:fail.append(os.fsdecode(path)+': index stage')
        indexed[path]=(mode,oid)
    if indexed!=expected:fail.append('index differs from commit tree')
    head=git(repo,'rev-parse','HEAD').decode().strip()
    if head!=rev:fail.append('HEAD differs')
    return dict(head=head,tree=git(repo,'rev-parse',rev+'^{tree}').decode().strip(),blob_files_checked=count,gitlinks=links,failures=fail)
head='4f6216abff01b6f859d348aaf6a71e47c5a5a2a8'; result={'superproject':check(root,head),'submodules':{}}
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
    pin=result['superproject']['gitlinks'][name];r=check(root/name,pin)
    superpath=git(root/name,'rev-parse','--show-superproject-working-tree').decode().strip()
    if pathlib.Path(superpath)!=root:r['failures'].append('not registered submodule')
    result['submodules'][name]=r
result['status']=git(root,'status','--porcelain=v1','--untracked-files=all').decode()
print(json.dumps(result,indent=2))
sys.exit(int(bool(result['superproject']['failures']) or any(r['failures'] for r in result['submodules'].values())))
