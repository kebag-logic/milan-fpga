#!/usr/bin/env python3
"""Verify every tracked byte, file type, executable mode, stage and initialized gitlink."""
import hashlib, json, os, pathlib, stat, subprocess, sys
env=os.environ.copy()
env['GIT_NO_REPLACE_OBJECTS']='1'
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],env=env)
def verify(root,expected,submodules=True):
    head=git(root,'rev-parse','HEAD').decode().strip()
    assert head==expected,(root,head,expected)
    records=git(root,'ls-tree','-rz',expected).split(b'\0')
    want={}; errors=[]; links={}; blobs=0
    for entry in filter(None,records):
        info,name=entry.split(b'\t',1)
        mode,typ,oid=info.split()
        name=os.fsdecode(name); file=root/name
        want[name]=(mode.decode(),oid.decode(),'0')
        if typ==b'commit':
            links[name]=oid.decode();continue
        blobs+=1
        try:
            s=file.lstat()
            if mode==b'120000':
                assert stat.S_ISLNK(s.st_mode)
                data=os.fsencode(os.readlink(file))
            else:
                assert stat.S_ISREG(s.st_mode)
                assert bool(s.st_mode & stat.S_IXUSR)==(mode==b'100755')
                data=file.read_bytes()
            got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert got==oid.decode()
        except (OSError,AssertionError):errors.append(name)
    actual={}
    for entry in filter(None,git(root,'ls-files','--stage','-z').split(b'\0')):
        info,name=entry.split(b'\t',1)
        mode,oid,stage=info.decode().split()
        name=os.fsdecode(name)
        assert name not in actual,'duplicate index stage'
        actual[name]=(mode,oid,stage)
    assert actual==want,'index differs from committed tree'
    assert not errors,errors
    result={'head':head,'tree':git(root,'rev-parse','HEAD^{tree}').decode().strip(),'blobs_verified':blobs,'index':'exact','bytes_and_modes':'exact','gitlinks':links}
    if submodules:
        result['submodules']={}
        for name,oid in links.items():
            if name=='external':
                result['submodules'][name]={'gitlink':oid,'checkout':'unused, not initialized'}
            else:result['submodules'][name]=verify(root/name,oid,False)
    return result
packet=pathlib.Path(__file__).resolve().parent
result={'stack':verify(pathlib.Path(sys.argv[1]),'5d14a6d816a43a49299172a34e3eeaea44c267c6'),
        'parent':verify(pathlib.Path(sys.argv[2]),'27495a06d5569336a098da20381ced3e331ba665')}
(packet/'receipts/exact-bytes.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
