#!/usr/bin/env python3
"""Independent size comparison and refusal probes; candidate sources never edited."""
import importlib.util,json,os,pathlib,shutil,struct,subprocess,sys
from unittest.mock import patch
repo=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parents[1]
work=packet/'scratch/independent';work.mkdir(exist_ok=True)
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
os.environ['TMPDIR']=str(packet/'scratch/tmp');os.environ['PYTHON_CPU_COUNT']='1'
cc=str(packet/'scratch/sdk/bin/riscv32-linux-gcc');os.environ['MILAN_RV32_CC']=cc
sys.path[:0]=[str(repo/p) for p in ['sw/firmware/gtest','sw/firmware/ctrl/test','sw/firmware/ctrl_nvm/test']]
import fw_rv32,ctrl_arms,ctrl_build,nvm_bench,nvm_rv32,test_ctrl_nvm
BASE='6714181d0c8a16e2983f85b724f4d688f5111835'
def call(argv):
 r=subprocess.run([str(a) for a in argv],capture_output=True,text=True)
 assert r.returncode==0,(argv,r.stderr)
 return r.stdout
def base_module(path,name):
 target=work/(name+'.py');target.write_text(call(['git','-C',repo,'show',BASE+':'+path]))
 spec=importlib.util.spec_from_file_location(name,target);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=base_module('sw/firmware/ctrl_nvm/test/nvm_rv32.py','baseline_nvm_rv32')
# Adding stack reporting does not alter generated code. Preserve every other baseline flag.
old.RV32_FLAGS=(*old.RV32_FLAGS,'-fstack-usage')
measurements=[]
for cfg in sorted((repo/'configs').glob('endstation_*.yaml')):
 inputs=nvm_bench.shape_inputs(cfg,work/cfg.stem/'inputs');gen=work/cfg.stem/'gen'
 nvm_bench.write_headers(gen,nvm_bench.shape_header(inputs.shape,inputs.donor,inputs.ident),inputs.clock_hz)
 before_dir=work/cfg.stem/'before';after_dir=work/cfg.stem/'after'
 before_find,before=old.build(nvm_bench.TREE,before_dir,gen,cc)
 after_find,after=nvm_rv32.build(nvm_bench.TREE,after_dir,gen,cc)
 assert not before_find and not after_find,(before_find,after_find)
 before['stack_frame']=fw_rv32.stack_frames(sorted(before_dir.glob('*.o')))
 assert before['text']-after['text']==240
 assert {k:v for k,v in before.items() if k!='text'}=={k:v for k,v in after.items() if k!='text'}
 print(cfg.stem,json.dumps({'before':before,'after':after},sort_keys=True),flush=True)
 measurements.append({'shape':cfg.stem,'before':before,'after':after})
# Reproduce the initial missing glibc-stub defect against the same SDK.
source=ctrl_build.CTRL/'port/ctrl_debug.c';obj=work/'original-ctrl.o'
flags=[x for x in ctrl_build.RV32_FLAGS if x!='-fstack-usage']
tree=ctrl_build.Tree(ctrl_build.CTRL,work/'ctrl',work/'reuse')
original=subprocess.run([cc,*flags,*ctrl_build.includes(tree),'-c',str(source),'-o',str(obj)],capture_output=True,text=True)
assert original.returncode and 'gnu/stubs-ilp32.h' in original.stderr,original.stderr
print('PASS: original ctrl header path fails on gnu/stubs-ilp32.h')
result=ctrl_arms.arm_rv32(tree,True);assert result.rc==0,result.log;print(result.log)
# Same baseline ctrl flags, isolated headers only: compare every code/data/relocation section.
base_objs=work/'ctrl-baseline-isolated';base_objs.mkdir(exist_ok=True)
for src in ctrl_build.sources(tree,ctrl_build.PORTABLE+('plat/mbx_plat_mmio.c',)):
 out=base_objs/f'{src.parent.name}_{src.stem}.o'
 call([cc,*flags,*fw_rv32.includes(cc),*ctrl_build.includes(tree),'-c',src,'-o',out])
 new=tree.out/'rv32'/out.name
 assert out.read_bytes()==new.read_bytes(),out.name
print('PASS: all 9 ctrl objects byte-identical with baseline flags plus isolated headers; stack reporting changes no object bytes')
# Required-compiler refusal includes the store arm, absent from the new control's direct check.
with patch.dict(os.environ,MILAN_RV32_CC=str(work/'absent')):
 try:test_ctrl_nvm.rv32_arm(inputs,work/'absent-build',True)
 except nvm_bench.Refusal:print('PASS: required store compiler is refused without fallback')
 else:raise AssertionError('required store compiler skipped')
# Actual arms must reject additional ISA attributes, even though compilation succeeds.
with patch.object(ctrl_arms,'RV32_FLAGS',tuple('-march=rv32im' if x=='-march=rv32i' else x for x in ctrl_arms.RV32_FLAGS)):
 result=ctrl_arms.arm_rv32(ctrl_build.Tree(ctrl_build.CTRL,work/'ctrl-m',work/'reuse'),True)
 assert result.rc==1 and 'architecture attribute' in result.log,result.log
print('PASS: actual ctrl arm rejects RV32M')
with patch.object(nvm_rv32,'RV32_FLAGS',tuple('-march=rv32im' if x=='-march=rv32i' else x for x in nvm_rv32.RV32_FLAGS)):
 findings,_=nvm_rv32.build(nvm_bench.TREE,work/'nvm-m',gen,cc)
 assert any('architecture attribute' in x for x in findings),findings
print('PASS: actual store arm rejects RV32M')
# Actual source mutation requires a dynamic frame refusal, independently of symbol refusal.
for label,srcroot,source_rel in [('ctrl',ctrl_build.CTRL,'port/ctrl_debug.c'),('nvm',nvm_bench.TREE,'nvm_klj2.c')]:
 target=work/(label+'-dynamic');shutil.copytree(srcroot,target)
 source=target/source_rel
 source.write_text(source.read_text()+'\nextern void consume_frame(void *);\nvoid dynamic_probe(unsigned n) { char buffer[n]; consume_frame(buffer); }\n')
 if label=='ctrl':
  got=ctrl_arms.arm_rv32(ctrl_build.Tree(target,work/'ctrl-dynamic-build',work/'reuse'),True)
  assert got.rc==1 and 'non-static stack usage' in got.log,got.log
 else:
  findings,_=nvm_rv32.build(target,work/'nvm-dynamic-build',gen,cc)
  assert any('non-static stack usage' in f for f in findings),findings
 print('PASS:',label,'actual arm rejects source-induced dynamic stack frame')
# ELF-format boundaries checked on real compiler output.
obj=next((tree.out/'rv32').glob('*.o'));original=obj.read_bytes()
for label,offset,data in [('big-endian',5,b'\x02'),('wrong-machine',18,struct.pack('<H',62)),('executable',16,struct.pack('<H',2)),('embedded-ABI',36,struct.pack('<I',8))]:
 copy=work/(label+'.o');bad=bytearray(original);bad[offset:offset+len(data)]=data;copy.write_bytes(bad)
 assert fw_rv32.object_findings(cc,[copy]),label
 print('PASS: rejected',label)
missing=work/'missing-frame.o'
try:fw_rv32.stack_frames([missing])
except OSError:print('PASS: missing frame file fails closed')
else:raise AssertionError('missing frame file accepted')
(packet/'receipts/object-size-comparison.json').write_text(json.dumps(measurements,indent=2)+'\n')
print('Independent RV32 probes PASS')
