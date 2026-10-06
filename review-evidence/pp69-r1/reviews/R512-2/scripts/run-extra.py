#!/usr/bin/env python3
import argparse,concurrent.futures,io,json,os,pathlib,shutil,subprocess,tarfile,time
p=argparse.ArgumentParser();p.add_argument('--count1-only',action='store_true');p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args();root=a.source.resolve();packet=a.packet.resolve();scratch=packet/'scratch';v=str(packet/'scripts/limited-simulator.py')
env=os.environ.copy();env['TMPDIR']=str(scratch);env['PYTHONDONTWRITEBYTECODE']='1';env['MAKEFLAGS']='-j16'
def run_probe(name,ref,depth):
 start=time.time();tree=scratch/name;tree.mkdir(exist_ok=True)
 with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',ref],cwd=root))) as t:t.extractall(tree,filter='data')
 shutil.copy2(packet/'scripts/reviewer-probe.cpp',tree/'reviewer-probe.cpp')
 flags='-std=c++17'+(' -DHEAD_SEAM' if ref=='HEAD' else '')+(' -DDEPTH16' if depth else '')
 cmd=[v,'--cc','--exe','--build','-j','2','--top-module','KL_aecp_notify','-GN_CTRL_P='+('16' if depth else '2'),'-GN_STREAM_IN_P=1','-GN_STREAM_OUT_P=1','-Wall','-Wno-fatal','-Wno-DECLFILENAME','-Wno-UNUSEDSIGNAL','-Wno-WIDTHEXPAND','-Wno-WIDTHTRUNC','-Wno-UNUSEDPARAM','-CFLAGS',flags,'hdl/common/pp_pkg.sv','hdl/aecp/KL_aecp_notify.sv','reviewer-probe.cpp','-o','Vprobe']
 if depth:cmd+=['-GN_IF_P=2']
 with (packet/'receipts'/f'{name}.log').open('w') as f:
  f.write(json.dumps({'ref':ref,'command':cmd})+'\n');f.flush();rc=subprocess.run(cmd,cwd=tree,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600).returncode
  if rc==0:rc=subprocess.run(['./obj_dir/Vprobe'],cwd=tree,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=120).returncode
 (packet/'receipts'/f'{name}.rc').write_text(str(rc)+'\n');print(name,rc,round(time.time()-start,1),flush=True);return rc
def docs():
 tree=scratch/'docs';subprocess.run(['git','clone','--quiet','--shared','--no-checkout',str(root),str(tree)],check=True);subprocess.run(['git','checkout','--quiet','--detach','75c4eee4589e9317aca3d07b91f94a38b4cc86af'],cwd=tree,check=True)
 with (packet/'receipts/docs-check.log').open('w') as f:rc=subprocess.run(['make','-j16','check'],cwd=tree,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=600).returncode
 (packet/'receipts/docs-check.rc').write_text(str(rc)+'\n');print('docs-check',rc,flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(4) as pool:
 jobs=[pool.submit(run_probe,'count1-base','e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8',False),pool.submit(run_probe,'count1-head','HEAD',False)]
 if not a.count1_only:jobs += [pool.submit(run_probe,'depth16','HEAD',True),pool.submit(docs)]
 rcs=[j.result() for j in jobs]
raise SystemExit(any(rcs))
