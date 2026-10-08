#!/usr/bin/env python3
import argparse,os,subprocess,json,hashlib,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path.cwd());ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--dependencies',type=Path,required=True);a=ap.parse_args();r=a.source.resolve();p=a.packet.resolve();dep=a.dependencies.resolve();runtime=p/'scratch/runtime'
env=dict(os.environ,MILAN_RV32_CC=str(p/'scratch/sdk/bin/riscv32-buildroot-linux-gnu-gcc'))
def run(argv):subprocess.run(argv,cwd=r,env=env,check=True)
run(['python3','sw/firmware/ctrl/test/ctrl_image_runtime.py','--picolibc',str(dep/'pythondata-software-picolibc/pythondata_software_picolibc/data'),'--compiler-rt',str(dep/'pythondata-software-compiler_rt/pythondata_software_compiler_rt/data'),'--litex-software',str(dep/'litex/litex/soc/software'),'--output',str(runtime)])
public=json.loads((p/'receipts/public-round10-sizes.json').read_text()); rows=[]
for expected in public['srp_images']:
 shape=expected['shape'];i=expected['interfaces'];out=p/'scratch'/f'image-{shape}-if{i}'
 run(['python3','sw/firmware/ctrl/test/ctrl_srp_image.py','--config',f'configs/{shape}.yaml','--interfaces',str(i),'--output',str(out),'--libc',str(runtime/'libc.a'),'--compiler-runtime',str(runtime/'libcompiler_rt.a')])
 actual=json.loads((out/'size.json').read_text());fields=['shape','interfaces','sections','static_storage','ram_sections','ram_span'];differences=[k for k in fields if actual[k]!=expected[k]]
 elf=next(x for x in actual['artifacts'] if x['name']=='ctrl_app.elf');expected_elf=next(x for x in expected['artifacts'] if x['name']=='ctrl_app.elf')
 if elf!=expected_elf:differences.append('ELF')
 rows.append({'shape':shape,'interfaces':i,'differences':differences,'actual':actual});print('IMAGE COMPARE',shape,i,differences,flush=True)
(p/'receipts/image-comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
prov=json.loads((runtime/'provenance.json').read_text());text=json.dumps(prov,indent=2).replace(str(dep),'$DEPENDENCIES').replace(str(p),'$PACKET');(p/'receipts/runtime-provenance.json').write_text(text+'\n')
assert all(not x['differences'] for x in rows)
