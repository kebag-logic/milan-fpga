"""Size preflight: unchanged four-protocol fixture plus the existing F1 store.

This is a link fixture only. State-owner callbacks remain stubs. No AECP,
map owner, descriptor image, board startup or hardware integration is added.
"""
import argparse, json, sys
from pathlib import Path
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("--root",type=Path,required=True)
ap.add_argument("--output",type=Path,required=True)
ap.add_argument("--runtime",type=Path,required=True)
ap.add_argument("--shape",required=True)
ap.add_argument("--interfaces",type=int,choices=(1,2),required=True)
a=ap.parse_args()
root=a.root.resolve(); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
sys.path[:0]=[str(root/"sw/firmware/ctrl/test"),str(root/"sw/firmware/ctrl_nvm/test")]
import ctrl_srp_image as image
import nvm_bench
nvm=root/"sw/firmware/ctrl_nvm"
config=root/"configs"/(a.shape+".yaml")
shape=nvm_bench.shape_inputs(config,out/"shape")
gen=out/"gen"
nvm_bench.write_headers(gen,nvm_bench.shape_header(shape.shape,shape.donor,shape.ident),shape.clock_hz)
source=(root/"sw/firmware/ctrl/test/ctrl_image.c").read_text()
stubs=(root/"sw/firmware/ctrl/test/rv32_image/image_main.c").read_text()
start=stubs.index("static int model_ready(")
end=stubs.index("#ifdef CTRL_APP_ACMP_FIRST_SLOT",start)
stubs=stubs[start:end]
headers='\n#include "nvm_flash_litespi.h"\n#include "nvm_store.h"\n'
source=source.replace('int main(void)',headers+stubs+'\nint main(void)',1)
source=source.replace('    const struct ctrl_app_config cfg = {','    nvm_flash_litespi_power_on();\n    nvm_store_boot(&nvm_flash_litespi, &others);\n    const struct ctrl_app_config cfg = {',1)
source=source.replace('    ctrl_loop_run(&image_app.loop);','    if (!ctrl_loop_add_tick(&image_app.loop, nvm_store_service)) return 3;\n    ctrl_loop_run(&image_app.loop);',1)
fixture=out/"fixture"; fixture.mkdir(exist_ok=True)
(fixture/"ctrl_image.c").write_text(source)
(fixture/"ctrl_image.ld").write_bytes((root/"sw/firmware/ctrl/test/ctrl_image.ld").read_bytes())
image.HERE=fixture
image.PORTABLE=(*image.PORTABLE,*(str(nvm/s) for s in ("nvm_klj2.c","nvm_store.c","plat/nvm_flash_litespi.c")))
image.RV32_FLAGS=(*image.RV32_FLAGS,f"-I{gen}",f"-I{nvm/'plat'}",f"-I{nvm/'test/rv32'}")
sys.argv=["ctrl_srp_image.py","--config",str(config),"--interfaces",str(a.interfaces),"--output",str(out),"--libc",str(a.runtime/"libc.a"),"--compiler-runtime",str(a.runtime/"libcompiler_rt.a")]
raise SystemExit(image.main())
