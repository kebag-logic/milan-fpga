#!/usr/bin/env python3
"""Reproduce base/head fixture placement without modifying either tree.
This proves present fixture applicability, not the time of the executor's pre-edit audit.
"""
import sys,subprocess,tarfile,io,importlib.util
from pathlib import Path

def one(root):
 sys.path.insert(0,str(root/'sw/mailbox'))
 import gen_mailbox
 from mailbox_model import load
 sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
 import ctrl_mutants
 spec=importlib.util.spec_from_file_location('rtl_mutants',root/'tb/verilator/mbx/mutants.py')
 m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 count=0
 for prefix,arms,base in [('RTL',m.ARMS,root/'hdl/milan/mailbox'),('firmware',ctrl_mutants.MUTANTS,root/'sw/firmware/ctrl')]:
  for a in arms:
   n=(base/a.path).read_text().count(a.old)
   assert n==1,(a.name,n)
   print(prefix,a.name,'plants once')
  count+=len(arms)
 for name,old,new in gen_mailbox._contract_arms():
  n=(root/'sw/mailbox/mailbox.yaml').read_text().count(old)
  assert n==1,(name,n)
  print('contract',name,'plants once')
 count+=len(gen_mailbox._contract_arms())
 arms=gen_mailbox._output_arms(load())
 for name,texts,needle in arms:
  assert any(needle in f for f in gen_mailbox.crosscheck(load(),texts)),name
  print('output',name,'plants and is detected')
 count+=len(arms)
 print('TOTAL',count)

if sys.argv[1]=='--single': one(Path(sys.argv[2]).resolve()); raise SystemExit()
root,work=map(lambda s:Path(s).resolve(),sys.argv[1:])
base=work/'base-fixtures';base.mkdir(parents=True,exist_ok=True)
raw=subprocess.check_output(['git','-C',str(root),'archive','6714181d0c8a16e2983f85b724f4d688f5111835'])
with tarfile.open(fileobj=io.BytesIO(raw)) as t: t.extractall(base,filter='data')
for label,tree in [('BASE',base),('HEAD',root)]:
 print(label,flush=True)
 subprocess.run([sys.executable,__file__,'--single',str(tree)],check=True)
# Exclusions must be byte-identical, including the ratchet's underlying definitions.
for path in ('sw/firmware/gtest/fw_coverage.py',):
 a=subprocess.check_output(['git','-C',str(root),'show','6714181d:'+path])
 assert a==(root/path).read_bytes(),path
 print(path,'unchanged')
keys=['KL_mbx','mbx_model','mailbox.yaml','mbx_contract','ctrl/mbx','ctrl/loop','ctrl/app']
for rel in ('','protocol-processor','gptp-processor','third_party/verilog-axis'):
 repo=root/rel
 args=['git','-C',str(repo),'grep','-n','-F']
 for k in keys: args+=['-e',k]
 args+=['--','*.patch']
 result=subprocess.run(args,capture_output=True,text=True)
 print('patch audit',rel or 'root','rc',result.returncode)
 print(result.stdout,end='')
 assert result.returncode==1,(rel,result.stderr)
print('PASS current base/head applicability and patch census')
