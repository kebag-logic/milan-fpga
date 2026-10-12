#!/usr/bin/env python3
import argparse,hashlib,json,os,pathlib,stat,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--source',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();src=a.source.resolve();p=a.packet.resolve()
def git(*args):return subprocess.check_output(['git',*args],cwd=src)
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();assert head=='1edff3180c2ff435b855cc770fb8be371f2096b3' and tree=='e08f8e9ba2a3732edbdd4c3656c46676355c41a6'
entries=[];links=[]
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not row:continue
 meta,name=row.split(b'\t',1);mode,kind,blob=meta.decode().split();path=name.decode()
 if kind=='commit':links.append(dict(path=path,sha=blob));continue
 f=src/path;data=os.readlink(f).encode() if f.is_symlink() else f.read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert actual==blob,path
 actualmode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode&stat.S_IXUSR else '100644');assert actualmode==mode,path
 entries.append(dict(path=path,mode=mode,blob=blob,sha256=hashlib.sha256(data).hexdigest()))
index=git('write-tree').decode().strip();assert index==tree
status=git('status','--porcelain=v2','--untracked-files=all').decode();assert not status
assert not links
ptree=json.loads((p/'scratch/fabric-tree.json').read_text());link=next(e for e in ptree['tree'] if e['path']=='protocol-processor');assert link['mode']=='160000' and link['sha']=='2ad2f845dd583f8310075fa2380cb60a04fd091a'
for e in json.loads((p/'receipts/fabric-inputs.json').read_text()):
 b=(p/'scratch/fabric'/e['path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob']
parent='hdl/milan/milan_datapath.sv';b=(p/'scratch/milan_datapath.sv').read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==next(e['sha'] for e in ptree['tree'] if e['path']==parent)
result=dict(head=head,tree=tree,index_tree=index,detached=subprocess.run(['git','symbolic-ref','-q','HEAD'],cwd=src,stdout=subprocess.DEVNULL).returncode==1,tracked_files=len(entries),entries=entries,gitlinks=links,status=status,parent_commit='c6bd08c6f52632c6d33d834ce842ac3cf63f29cc',processor_gitlink=link['sha'],parent_consumer_blob=blob,scoped_fabric_blobs_verified=7)
(p/'receipts/source-after.json').write_text(json.dumps(result,indent=2)+'\n');print('Exact head, tree, index,',len(entries),'blob bytes and modes; clean; no core gitlinks; parent processor gitlink and seven scoped blobs verified')
