#!/usr/bin/env python3
"""Verify every tracked worktree byte/mode and every index entry against the head."""
import argparse,hashlib,json,os,stat,subprocess
from pathlib import Path
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    def git(*args):return subprocess.check_output(['git','-C',str(a.repo),*args])
    head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
    assert head=='c4539ff107a6a4c7d2e4a4844182b00a2bf33c82'
    assert tree=='4378652558345d65dd87efd4f092f41f413226c8'
    entries=[];problems=[];links=[];expected={}
    for raw in git('ls-tree','-rz','--full-tree',head).split(b'\0'):
        if not raw:continue
        meta,path=raw.split(b'\t',1);mode,typ,oid=meta.decode().split();rel=os.fsdecode(path);expected[rel]=(mode,oid)
        if mode=='160000':
            actual=subprocess.check_output(['git','-C',str(a.repo/rel),'rev-parse','HEAD']).decode().strip();links.append({'path':rel,'expected':oid,'actual':actual})
            if actual!=oid:problems.append('gitlink '+rel)
            continue
        f=a.repo/rel;st=f.lstat()
        data=os.fsencode(os.readlink(f)) if stat.S_ISLNK(st.st_mode) else f.read_bytes()
        actual_mode='120000' if stat.S_ISLNK(st.st_mode) else ('100755' if st.st_mode&0o111 else '100644')
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        ok=actual==oid and actual_mode==mode
        if not ok:problems.append('blob or mode '+rel)
        entries.append({'path':rel,'blob':actual,'mode':actual_mode,'matches_head':ok})
    actual_index={}
    for raw in git('ls-files','--stage','-z').split(b'\0'):
        if not raw:continue
        meta,path=raw.split(b'\t',1);mode,oid,stage=meta.decode().split();rel=os.fsdecode(path)
        if stage!='0':problems.append('index stage '+rel)
        actual_index[rel]=(mode,oid)
    if actual_index!=expected:problems.append('index entries differ')
    status=git('status','--porcelain=v1','--untracked-files=all').decode()
    if status:problems.append('nonempty status')
    result={'head':head,'tree':tree,'tracked_blobs':len(entries),'all_blob_bytes_and_modes_match':not problems,'index_matches':actual_index==expected,'gitlinks':links,'status':status,'problems':problems,'entries':entries}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='entries'},indent=2));return bool(problems)
if __name__=='__main__':raise SystemExit(main())
