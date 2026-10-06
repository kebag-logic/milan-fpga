#!/usr/bin/env python3
"""Focused sequential equivalence of both changed arbiter forms, with a tie fault control."""
import argparse,concurrent.futures,pathlib,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();r=a.repo.resolve();p=a.packet.resolve();s=p/'scratch/equivalence';s.mkdir(exist_ok=True);logs=p/'receipts/equivalence';logs.mkdir(exist_ok=True)
f='hdl/packet_engine/KL_pp_tx_arbiter.sv';base=subprocess.check_output(['git','show','86a7b0c5:'+f],cwd=r,text=True);head=(r/f).read_text();mut=head.replace('(key_w[j] <= key_w[i])','(key_w[j] < key_w[i])');assert mut!=head
for name,source in [('base',base),('head',head),('tie-fault',mut)]:
 (s/(name+'.sv')).write_text(source)
 with (s/(name+'.v')).open('w') as out:subprocess.run(['sv2v',str(r/'hdl/common/pp_pkg.sv'),str(s/(name+'.sv'))],stdout=out,check=True)
def proof(name,variant,params):
 script=[]
 for role,src in [('gold','base'),('gate',variant)]:
  script+=['read_verilog '+str(s/(src+'.v'))]
  if params:script+=['chparam -set N_REQ_P 8 -set PRIO_MAP_P 30409 -set SOLICITED_MASK_P 165 KL_pp_tx_arbiter']
  script+=['prep -top KL_pp_tx_arbiter','memory_map','opt','rename KL_pp_tx_arbiter '+role,'design -stash '+role]
 script+=['design -copy-from gold -as gold gold','design -copy-from gate -as gate gate','equiv_make gold gate equiv','hierarchy -top equiv','equiv_simple -seq 2','equiv_induct -seq 2','equiv_status -assert']
 path=s/(name+'.ys');path.write_text('\n'.join(script)+'\n')
 with (logs/(name+'.log')).open('w') as out:rc=subprocess.run(['yosys','-Q','-s',str(path)],stdout=out,stderr=subprocess.STDOUT).returncode
 (logs/(name+'.rc')).write_text(str(rc)+'\n');print(name,'rc',rc,flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(3) as pool:
 result=list(pool.map(lambda x:proof(*x),[('defaults','head',False),('top-eight-lanes','head',True),('tie-fault-control','tie-fault',True)]))
assert result[0]==0 and result[1]==0 and result[2]!=0,result
