"""Compare source bytes/modes/index with A164's captured starting head."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
repo=Path.cwd(); label=sys.argv[1]
old=json.loads((root/'original-integrity.json').read_text())
def git(*args):
    return subprocess.check_output(['git',*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'))
entries=[]
for row in git('ls-files','--stage','-z').split(b'\0'):
    if not row:continue
    meta,name=row.split(b'\t');mode,oid,stage=meta.decode().split();path=os.fsdecode(name)
    assert stage=='0'
    if mode=='160000':
        entries.append(dict(path=path,mode=mode,blob=oid,gitlink=True));continue
    p=repo/path;data=os.readlink(p).encode() if p.is_symlink() else p.read_bytes()
    actual_mode='120000' if p.is_symlink() else ('100755' if p.stat().st_mode & stat.S_IXUSR else '100644')
    assert actual_mode==mode,(path,actual_mode,mode)
    entries.append(dict(path=path,mode=mode,blob=oid,sha256=hashlib.sha256(data).hexdigest(),worktree_blob=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()))
previous={x['path']:x for x in old['files']};current={x['path']:x for x in entries}
assert previous.keys()==current.keys()
changed=[]
for name,row in current.items():
    base=previous[name];assert base['mode']==row['mode']
    if row.get('gitlink'):assert row==base
    elif base['sha256']!=row['sha256']:changed.append(name)
assert sorted(changed)==['docs/DOC_GENERATION.md','scripts/gen_toc.py','scripts/gen_toc_closer_cases.py'],changed
original=(root/'original/scripts/gen_toc.py').read_bytes()
assert original.replace(b'MIN_ARMS = 683',b'MIN_ARMS = 707')==Path('scripts/gen_toc.py').read_bytes()
assert old['index_flags']==git('ls-files','-v').decode()
index_entries=git('ls-files','--stage').decode()
if label=='precommit':assert old['index_entries']==index_entries
else:
    assert all(x.get('gitlink') or x['blob']==x['worktree_blob'] for x in entries)
    assert not git('status','--porcelain=v1')
index=Path(git('rev-parse','--git-path','index').decode().strip())
record={'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'status':git('status','--porcelain=v2','--branch').decode(),'changed_paths':changed,'non_test_non_doc_bytes_unchanged':True,'gen_toc_only_floor_changed':True,'file_modes_unchanged':True,'index_flags_unchanged':True,'index_entries':index_entries,'index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'files':entries}
(root/(label+'-integrity.json')).write_text(json.dumps(record,indent=2)+'\n')
print({k:v for k,v in record.items() if k not in ('files','index_entries')})
