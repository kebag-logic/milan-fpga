#!/usr/bin/env python3
"""Check whether a private definition can hide another object's open runtime symbol."""
import json,os,pathlib,shutil,subprocess,sys
repo=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parents[1]
work=packet/'scratch/runtime-binding';work.mkdir(parents=True,exist_ok=True)
os.environ.update(MILAN_RV32_CC=str(packet.parent/'sdk/bin/riscv32-linux-gcc'),TMPDIR=str(packet/'scratch/tmp'),PYTHON_CPU_COUNT='1');sys.dont_write_bytecode=True
sys.path[:0]=[str(repo/p) for p in ['sw/firmware/gtest','sw/firmware/ctrl/test','sw/firmware/ctrl_nvm/test']]
import ctrl_build,ctrl_arms,nvm_bench,nvm_rv32
cc=os.environ['MILAN_RV32_CC'];symbol='__review_runtime_service'
caller=f'\nextern void *{symbol}(__SIZE_TYPE__);\nvoid *review_runtime_probe(void) {{ return {symbol}(16); }}\n'
local=f'\n__attribute__((used)) static void *{symbol}(__SIZE_TYPE__ n) {{ (void)n; return (void *)0; }}\n'
results=[]
for label,root,callfile,privatefile in [('ctrl',ctrl_build.CTRL,'port/shlan_port.c','port/ctrl_debug.c'),('nvm',nvm_bench.TREE,'nvm_klj2.c','nvm_store.c')]:
 tree=work/label;shutil.copytree(root,tree)
 target=tree/callfile;target.write_text(target.read_text()+caller)
 if label=='nvm':
  inputs=nvm_bench.shape_inputs(repo/'configs/endstation_ax7101_1x1_tdm8.yaml',work/'inputs');gen=work/'gen'
  nvm_bench.write_headers(gen,nvm_bench.shape_header(inputs.shape,inputs.donor,inputs.ident),inputs.clock_hz)
 def build(tag):
  out=work/(label+'-'+tag)
  if label=='ctrl':
   result=ctrl_arms.arm_rv32(ctrl_build.Tree(tree,out,work/'reuse'),True);return result.rc,result.log,out/'rv32'
  found,sizes=nvm_rv32.build(tree,out,gen,cc);return int(bool(found)),json.dumps({'findings':found,'sizes':sizes}),out
 rc,log,_=build('open');assert rc and symbol in log,(label,log)
 print(label,'unresolved-symbol positive control: REJECTED',flush=True)
 target=tree/privatefile;target.write_text(target.read_text()+local)
 rc,log,objects=build('masked');print(label,'with same-named static function: rc',rc);print(log)
 merged=work/(label+'-partial.o')
 result=subprocess.run([cc.removesuffix('gcc')+'ld','-m','elf32lriscv','-r','-o',str(merged),*map(str,sorted(objects.glob('*.o')))],capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 actual=subprocess.check_output([cc.removesuffix('gcc')+'nm','-u',str(merged)],text=True)
 assert symbol in actual,actual
 print(label,'partial link still has unresolved runtime dependency:',symbol)
 results.append({'arm':label,'ordinary_unresolved_refused':True,'masked_arm_rc':rc,'partial_link_symbol_remains_undefined':True})
(packet/'receipts/runtime-binding-result.json').write_text(json.dumps(results,indent=2)+'\n')
print('Runtime-binding probe complete')
