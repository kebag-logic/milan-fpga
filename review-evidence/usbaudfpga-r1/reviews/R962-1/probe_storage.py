#!/usr/bin/env python3
"""Plant loss of the low subslot byte in each actual shared storage path."""
import argparse,concurrent.futures,json,os,resource,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--engine',required=True);a=p.parse_args()
root=a.repo.resolve();packet=a.packet.resolve();resource.setrlimit(resource.RLIMIT_CORE,(0,0))
plants=[('mapper','KL_chan_map_capture.sv','tdm_pair_w  = {tdm_l_i, tdm_r_i};',"tdm_pair_w  = {tdm_l_i[31:8], 8'd0, tdm_r_i[31:8], 8'd0};",'CAPTURE_STORAGE_ALL_BITS'),('packetizer','KL_aaf_packetizer.sv',"(SAMPLE_BITS_P == 32) ? buf_l_r[j][7:0] : 8'h00","8'h00",'AAF_STORAGE_ALL_BITS'),('render','KL_render_queue.sv','odd_w[7:0], odd_w[15:8], odd_w[23:16], odd_w[31:24]',"8'd0, odd_w[15:8], odd_w[23:16], odd_w[31:24]",'')]
def run(plant):
 name,leaf,old,new,check=plant;out=packet/'scratch'/('probe-'+name);out.mkdir(parents=True,exist_ok=False)
 sources=[]
 for f in ['KL_chan_map_capture.sv','KL_aaf_packetizer.sv','KL_render_queue.sv']:
  text=(root/'hdl/ieee1722/aaf'/f).read_text()
  if f==leaf:
   assert text.count(old)==1,(f,text.count(old));text=text.replace(old,new)
  dest=out/f;dest.write_text(text);sources.append(str(dest))
 if name=='render':
  cmd=['make','-j16','-C',str(root/'tb/verilator/render_queue'),'build','VERILATOR='+a.engine,'VERILATOR_JOBS=2','SAMPLE_BITS=32','SRCS='+str(out/leaf),'CPP='+str(root/'tb/verilator/render_queue/sim_main.cpp'),'MDIR='+str(out/'build')];exe=out/'build/VKL_render_queue_sim'
 else:
  cmd=[a.engine,'--binary','--timing','--top-module','storage_tb','-GWIDTH_P=32','-Wall','-Wno-fatal','-Wno-TIMESCALEMOD','--build-jobs','2','--Mdir',str(out/'build'),*sources[:2],str(root/'tb/verilator/usbaudio/storage_tb.sv')];exe=out/'build/Vstorage_tb'
 with (out/'compile.log').open('w') as log:c=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 if c.returncode: return {'plant':name,'result':'BUILD_FAILED'}
 r=subprocess.run([str(exe)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
 (packet/'receipts'/('probe-'+name+'.log')).write_text(r.stdout)
 caught=r.returncode!=0 and (('CHECK '+check) in r.stdout if check else 'failures: 0' not in r.stdout and 'FAIL' in r.stdout)
 return {'plant':name,'compiled':True,'rc':r.returncode,'named_check':check or 'render_queue byte oracle','caught':caught}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,plants))
(packet/'receipts/storage-probes.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results))
raise SystemExit(0 if all(r.get('caught') for r in results) else 1)
