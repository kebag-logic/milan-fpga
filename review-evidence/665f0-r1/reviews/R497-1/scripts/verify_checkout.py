#!/usr/bin/env python3
"""Verify tracked file bytes, modes, index and required gitlinks without changing them."""
import hashlib,os,pathlib,stat,subprocess,sys
r=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(__file__).resolve().parents[1]
head='0bfef4987eede4b022b17c7b2f56d079ff84893b';base='fa450d301805881ad713b67521477bf042ddadfd'
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args])
def verify(repo,expected):
    actual=git(repo,'rev-parse','HEAD').decode().strip();assert actual==expected,(actual,expected)
    tree={}
    for row in git(repo,'ls-tree','-rz','HEAD').split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,typ,oid=meta.decode().split();tree[os.fsdecode(path)]=(mode,oid)
    index={}
    for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0'
        index[os.fsdecode(path)]=(mode,oid)
    assert index==tree,'index differs from HEAD'
    checked=0
    for name,(mode,oid) in tree.items():
        if mode=='160000':continue
        file=repo/name;st=file.lstat()
        if mode=='120000':assert stat.S_ISLNK(st.st_mode);data=os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(st.st_mode),name
            actualmode='100755' if st.st_mode & 0o111 else '100644';assert actualmode==mode,name
            data=file.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest==oid,'tracked bytes differ: '+name;checked+=1
    print(repo.name,actual,'tracked_blobs=',checked,'bytes/modes/index PASS')
    return tree
tree=verify(r,head);assert git(r,'rev-parse','HEAD^{tree}').decode().strip()=='8fb1fca2c81b8fd79ba6daefe1147be4531088f4'
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
    assert tree[name][0]=='160000';verify(r/name,tree[name][1])
print('External optional submodule not initialized; HEAD gitlink preserved in index.')
print('Default shipping input diff:')
paths=['sw/firmware/milan_baremetal','sw/builder','configs','avdecc']
diff=git(r,'diff','--name-status',base+'..'+head,'--',*paths);print(diff.decode() or '(empty)');assert not diff
for path in paths:
    try:
        a=git(r,'rev-parse',base+':'+path).decode().strip();b=git(r,'rev-parse',head+':'+path).decode().strip()
    except subprocess.CalledProcessError:continue
    assert a==b;print(path,'base=head',a)
print('lwSRP pinned checkout:')
lwsrp=p/'scratch/lwsrp';pin=git(lwsrp,'rev-parse','19f5796b^{commit}').decode().strip();verify(lwsrp,pin)
print('No lwSRP implementation vendored in PR diff:')
names=git(r,'diff','--name-only',base+'..'+head).decode().splitlines()
assert not any('/lwsrp/' in n.lower() or '/lwSRP/' in n for n in names)
print('PASS; only caller port and integration test sources added.')
print('Working-tree status:');print(git(r,'status','--short','--untracked-files=normal').decode() or '(clean)')
