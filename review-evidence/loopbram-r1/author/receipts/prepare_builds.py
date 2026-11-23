import sys,json,subprocess,os
from pathlib import Path
root=Path('$CHECKOUT')
work=Path('$SCRATCH/builds')
work.mkdir(exist_ok=True)
sys.path.insert(0,str(root/'tb/verilator/ctrl_split_boot'))
import run as boot
import plat_ledger
archives=boot.runtime(work)
for name in ('endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8'):
 csr,flash=plat_ledger.maps(work,name)
 for mode in ('off','on'):
  cfg=root/'configs'/f'{name}.yaml' if mode=='off' else work.parent/f'{name}.yaml'
  out=work/(name+'-'+mode)
  args=[sys.executable,'-B',str(root/'sw/firmware/ctrl/test/ctrl_plat_image.py'),
   '--config',str(cfg),'--csr-csv',str(csr),'--flash-map',str(flash),'--output',str(out),
   '--libc',str(archives[0]),'--compiler-runtime',str(archives[1])]
  if '8x8' in name:args+=['--ledgered-point','platform-8x8-one-interface']
  with (work/(name+'-'+mode+'.log')).open('w') as log:
   rc=subprocess.run(args,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=3600).returncode
  print(name,mode,'LINK',rc,flush=True)
  (work/(name+'-'+mode+'.rc')).write_text(str(rc))
  if not (out/'ctrl_app.elf').exists(): raise RuntimeError('no linked ELF')
  (out/'inputs.json').write_text(json.dumps({'config':str(cfg),'csr':str(csr),'flash':str(flash),'args':args},indent=2))
