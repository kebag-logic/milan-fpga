import sys,json,hashlib,subprocess
from pathlib import Path
root=Path.cwd()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build
sys.path.insert(0,str(root/'sw/builder'))
import endstation_builder as eb
out=Path('$VALIDATION_STORAGE/artysplit-a829/r4/arty-product')
for shape in ('endstation_arty_split',):
    work=out/shape
    work.mkdir(parents=True,exist_ok=True)
    art=eb.build(str(root/'configs'/f'{shape}.yaml'),outdir=str(out/'generated'),placement='split')
    flash=work/'soc-map'
    if not (work/'mapped/soc/csr.csv').exists(): flash=build.flash_map(flash,shape)
    runtime=work/'mapped/runtime'
    argv=[sys.executable,'-B',str(root/'sw/firmware/ctrl/test/ctrl_plat_image.py'),'--config',str(root/'configs'/f'{shape}.yaml'),'--csr-csv',str(work/'mapped/soc/csr.csv'),'--flash-map',str(flash),'--output',str(work/'product'),'--libc',str(runtime/'libc.a'),'--compiler-runtime',str(runtime/'libcompiler_rt.a')]
    build.run(argv,work/'product.log',cwd=root)
    print('ARTY-PROVISIONAL',shape,hashlib.sha256((work/'product/ctrl_app.elf').read_bytes()).hexdigest(),flush=True)
