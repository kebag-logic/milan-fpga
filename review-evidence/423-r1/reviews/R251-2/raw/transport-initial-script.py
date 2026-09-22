"""Independent raw-tree probes in fresh, measured filesystem encodings."""
import argparse
import codecs
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('output',type=Path)
p.add_argument('--child')
a=p.parse_args()
a.checkout=a.checkout.resolve()
a.output=a.output.resolve()
a.output.mkdir(parents=True,exist_ok=True)

if not a.child:
    records=[]
    with tempfile.TemporaryDirectory(prefix='r251-transport-') as td:
        work=Path(td)
        locale_root=work/'locales'
        locale_root.mkdir()
        cmd=['rtk','proxy','localedef','--no-archive','-i','en_US','-f','ISO-8859-1',str(locale_root/'en_US.ISO-8859-1')]
        r=subprocess.run(cmd,capture_output=True)
        (a.output/'localedef.stdout').write_bytes(r.stdout)
        (a.output/'localedef.stderr').write_bytes(r.stderr)
        assert r.returncode==0,('Latin-1 NOT RUN',r.stderr)
        env=dict(os.environ,PYTHONCOERCECLOCALE='0',PYTHONUTF8='0',
                 PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8:backslashreplace',
                 GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,
                 GIT_AUTHOR_NAME='Review',GIT_AUTHOR_EMAIL='review@example.invalid',
                 GIT_COMMITTER_NAME='Review',GIT_COMMITTER_EMAIL='review@example.invalid')
        for encoding,locale in [('utf-8','C.UTF-8'),('ascii','C'),('iso8859-1','en_US.ISO-8859-1')]:
            # Repository path also contains real multibyte/invalid bytes.
            raw_path=os.fsencode(work)+b'/'+encoding.encode()+b'-\xc3\xa9-\xff'
            os.mkdir(raw_path)
            child_env=dict(env,LC_ALL=locale,LOCPATH=str(locale_root))
            cmd=['rtk','proxy','python3','-B',str(Path(__file__).resolve()),str(a.checkout),str(a.output),'--child',encoding]
            r=subprocess.run(cmd,cwd=raw_path,env=child_env,capture_output=True)
            (a.output/(encoding+'.stdout')).write_bytes(r.stdout)
            (a.output/(encoding+'.stderr')).write_bytes(r.stderr)
            records.append({'encoding':encoding,'argv':cmd,'cwd_bytes':raw_path.hex(),'exit':r.returncode,
                            'environment':{k:child_env[k] for k in ['LC_ALL','LOCPATH','PYTHONUTF8','PYTHONCOERCECLOCALE']}})
            print(encoding,'exit',r.returncode,flush=True)
            assert r.returncode==0,r.stderr
    (a.output/'processes.json').write_text(json.dumps(records,indent=2)+'\n')
    raise SystemExit(0)

actual=codecs.lookup(sys.getfilesystemencoding()).name
assert actual==a.child,(actual,a.child)
sys.path.insert(0,str(a.checkout/'scripts'))
import check_merge_containment as mc
import merge_containment_replay as proof

def raw(*args,data=None):
    return subprocess.run(['rtk','proxy','git','--no-replace-objects',*args],input=data,
                          capture_output=True,check=True).stdout

names=(b'\xc3\xa9.txt',b'raw-\xff.txt',b'\xe2\x82\xac.txt',b'\xf0\x9f\x8e\xb5.txt',b':(exclude)tab\tcr\r\nend\n')
alias=b'\xe9.txt'
old=b''.join(f'line {i:02d}\r\n'.encode() for i in range(50))+b'raw-\xff\r\nlast-no-newline'
changed=old.replace(b'line 07',b'changed \xff \xc3\xa9 07')
far=changed.replace(b'line 41',b'far extension 41')
raw('init','-q','-b','main')

def tree(payload,control):
    entries={n:payload+b'\r\n'+n.hex().encode() for n in names}
    entries.update({alias:b'unchanged and distinct alias\r\n','control'.encode():control})
    records=[]
    for name,data in entries.items():
        oid=raw('hash-object','-w','--stdin',data=data).strip()
        records.append(b'100644 blob '+oid+b'\t'+name+b'\0')
    return raw('mktree','-z',data=b''.join(records)).strip().decode()

def commit(tree,parents,label):
    args=['commit-tree',tree,'-m',label]
    for parent in parents:args.extend(['-p',parent])
    return raw(*args).strip().decode()

origin=commit(tree(old,old),[],'origin')
source_tree=tree(changed,old)
source=commit(source_tree,[origin],'source linear')
missing=commit(tree(old,far),[origin],'missing all named work')
linear_positive=commit(tree(changed,far),[origin],'retained linear work')
merge=commit(source_tree,[origin,source],'source redundant merge')
final_tree=tree(changed,changed)
branch=commit(final_tree,[merge],'source second')
replay_a=commit(source_tree,[origin],'distinct replay A')
replay_c=commit(final_tree,[replay_a],'distinct replay C')
reverted=commit(tree(old,far),[replay_c],'revert named work')
extended=commit(tree(changed,far),[replay_c],'retain with far extension')

rows=[]
calls=[]
real_run=subprocess.run

def tracing_run(argv,*args,**kwargs):
    r=real_run(argv,*args,**kwargs)
    if argv and argv[0]=='git':
        data=kwargs.get('input')
        calls.append({'argv_bytes':[os.fsencode(v).hex() for v in argv],
                      'input_hex':data.hex() if isinstance(data,bytes) else None,
                      'stdout_hex':r.stdout.hex() if isinstance(r.stdout,bytes) else None,'exit':r.returncode})
    return r

def check(label,got,want):
    rows.append({'label':label,'got':got,'expected':want,'pass':got==want})
    assert got==want,(label,got,want)

with patch.object(subprocess,'run',tracing_run):
    paths,error=mc._commit_paths(source)
    check('enumerated bytes',[error,sorted(os.fsencode(s).hex() for s in paths)], [None,sorted(n.hex() for n in names)])
    check('shared unequal postimage',list(mc._same_patch_postimage(source,origin)),[False,None])
    check('shared path proof refuses missing work',mc._path_scoped_verdict(source,missing,origin,1),None)
    for name in names:
        path=os.fsdecode(name)
        direct=raw(b'--literal-pathspecs',b'ls-tree',b'-z',b'--full-tree',source.encode(),b'--',name)
        expected=tuple(direct.split(b'\t')[0].decode().split())
        check('entry '+name.hex(),proof._tree_entry(source,path),expected)
    expected_patch=raw('show',*mc.RAW_DIFF_FLAGS,'--format=medium','--binary','--full-index','--no-renames',source).rstrip(b'\n')
    patch_id,error=mc._verbatim_patch_id(source)
    actual_patch=bytes.fromhex(next(c['input_hex'] for c in reversed(calls) if b'patch-id'.hex() in c['argv_bytes']))
    check('exact patch inverse',actual_patch==expected_patch,True)
    check('CRLF preserved in patch',b'\r\n' in actual_patch,True)
    check('invalid bytes preserved in patch',b'\xff' in actual_patch,True)
    check('verbatim ID',[patch_id,error],[raw('patch-id','--verbatim',data=expected_patch).split()[0].decode(),None])
    check('retention lists original paths',sorted(proof._retained_at_tip(branch,reverted,mc._git)),sorted(repr(os.fsdecode(n)) for n in names))
    check('retention positive',proof._retained_at_tip(branch,extended,mc._git),[])
    # Deliberately return a different byte name, a bad oid and multiple records.
    entry=raw(b'--literal-pathspecs',b'ls-tree',b'-z',b'--full-tree',source.encode(),b'--',names[0])
    bad_records=[entry.replace(names[0],alias),entry.replace(entry.split()[2].split(b'\t')[0],b'g'*40),entry+entry]
    for i,bad in enumerate(bad_records):
        refused=False
        with patch.object(proof,'_git_bytes',return_value=(0,bad)):
            try:proof._tree_entry(source,os.fsdecode(names[0]))
            except proof._MeasurementError:refused=True
        check('returned record refusal '+str(i),refused,True)
    # Git's path result can itself contain raw non-ASCII repository bytes.
    with patch.dict(os.environ,{'GIT_DIR':os.path.abspath('.git')}):
        check('graft path absent',mc.active_graft_error(),None)
        Path('.git/info/grafts').write_bytes(source.encode()+b'\n')
        check('graft path active', 'legacy Git grafts are active' in mc.active_graft_error(),True)
        Path('.git/info/grafts').unlink()

for label,source_oid,target,want in [('linear-missing',source,missing,[1,'STRANDED']),
                                   ('linear-positive',source,linear_positive,[0,'contained']),
                                   ('merge-reverted',branch,reverted,[1,'UNKNOWN']),
                                   ('merge-positive',branch,extended,[0,'contained'])]:
    r=real_run(['rtk','proxy','python3','-B',str(a.checkout/'scripts/check_merge_containment.py'),
                '--no-fetch','--base',target,source_oid],capture_output=True)
    (a.output/(a.child+'-'+label+'.stdout')).write_bytes(r.stdout)
    (a.output/(a.child+'-'+label+'.stderr')).write_bytes(r.stderr)
    check(label,[r.returncode,r.stdout.split()[0].decode()],want)
    if label=='merge-positive':check('positive fallback',b'raw no-op retention' in r.stdout,True)

for name in names:
    check('literal argv bytes '+name.hex(),any(name.hex() in c['argv_bytes'] for c in calls),True)
(a.output/(a.child+'-gitcalls.json')).write_text(json.dumps(calls,indent=2)+'\n')
(a.output/(a.child+'-checks.json')).write_text(json.dumps({'encoding':actual,'rows':rows,
    'patch_sha256':hashlib.sha256(expected_patch).hexdigest(),'names_hex':[n.hex() for n in names],
    'alias_hex':alias.hex()},indent=2)+'\n')
print('PASS',actual,len(rows),'independent checks')
