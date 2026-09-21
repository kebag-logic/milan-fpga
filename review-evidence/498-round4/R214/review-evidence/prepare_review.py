import os,shutil
from pathlib import Path
root=Path(__file__).resolve().parent.parent;tmp=Path(os.environ['REVIEW_TMP'])
for d in ['tmp','absent-home','absent-bin','elf-home','elf-bin','ccache']:(tmp/d).mkdir(parents=True,exist_ok=True)
for mode in ['absent','elf']:
 for directory in os.environ['PATH'].split(':'):
  p=Path(directory)
  if not p.is_dir():continue
  for f in p.iterdir():
   if not f.is_file() or not os.access(f,os.X_OK):continue
   if f.name.startswith('riscv') and not (mode=='elf' and f.name.startswith('riscv64-elf')):continue
   dest=tmp/(mode+'-bin')/f.name
   if not dest.exists():dest.symlink_to(f.absolute())
stage=tmp/'pp-stage'
for rel in ['hdl','protocol-processor','gptp-processor','third_party/verilog-axis','tb/common','tb/verilator/pp_shadow','tb/verilator/milan_dp','configs','scripts']:
 dest=stage/rel
 if not dest.exists():shutil.copytree(root/rel,dest,ignore=shutil.ignore_patterns('.git','__pycache__','obj_*'),symlinks=False)
p=stage/'tb/verilator/pp_shadow/Makefile';p.write_text(p.read_text().replace('--build -j 0','--build -j 8'))
