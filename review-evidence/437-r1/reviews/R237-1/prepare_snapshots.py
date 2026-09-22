import subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent;REPO=Path('$VALIDATION_STORAGE/reviews/r237-437-r1')
for label,rev in [('base','88e9276b2a220c716f64a843f7e1eb8f9265e896'),('head','65df1df50a80cd5f540a93d8f0cfabc97da3da75')]:
 root=OUT/'scratch'/label;root.mkdir(parents=True,exist_ok=True)
 files=subprocess.check_output(['rtk','proxy','git','-C',str(REPO),'ls-tree','-r','--name-only',rev,'scripts'],text=True).splitlines()
 for name in files:
  if Path(name).name.startswith('gen_toc') or Path(name).name=='check_em_dash.py':
   (root/Path(name).name).write_bytes(subprocess.check_output(['rtk','proxy','git','-C',str(REPO),'show',rev+':'+name]))
print('Base/head parser and consumer snapshots copied from committed Git blobs.')
