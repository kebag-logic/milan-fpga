#!/usr/bin/env python3
"""Verify every tracked byte, executable mode, index entry and gitlink."""
import argparse,hashlib,json,os,pathlib,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args();r=a.repo.resolve()
def git(*cmd):return subprocess.check_output(['git','-C',str(r),*cmd])
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();rows=[];links=[]
for entry in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not entry:continue
 meta,path=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();name=path.decode()
 if kind=='commit':links.append({'path':name,'oid':oid,'mode':mode});continue
 f=r/name;data=os.readlink(f).encode() if mode=='120000' else f.read_bytes();digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();actual='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644');rows.append({'path':name,'mode':mode,'blob':oid,'bytes_equal':digest==oid,'mode_equal':mode==actual})
index=git('ls-files','--stage','-z');expected=b''.join((x['mode']+' '+x['blob']+' 0\t'+x['path']).encode()+b'\0' for x in rows);base_links=[x.decode() for x in git('ls-tree','-r','ae982af85ec97286bd35b39403926d8f0eaec81d').splitlines() if x.startswith(b'160000')]
result={'head':head,'tree':tree,'head_matches':head=='625b001173fda5f6401af1dceaef8d8ab86f5ae9','tree_matches':tree=='ac1ad256022bde4758d180a1f938da81ed7cbed6','tracked_blobs':len(rows),'files':rows,'index_matches_head':index==expected,'head_gitlinks':links,'base_gitlinks':base_links,'status':git('status','--porcelain=v2').decode()};a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='files'}));raise SystemExit(not result['head_matches'] or not result['tree_matches'] or not result['index_matches_head'] or bool(result['status']) or not all(x['bytes_equal'] and x['mode_equal'] for x in rows))
