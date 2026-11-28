"""Link the product split image for one config, as round 9's product.py does: flash map from the
split SoC export, then ctrl_plat_image.py against it. usage: product.py <config-stem> <outdir>"""
import sys, hashlib, shutil
from pathlib import Path
import os
ROOT = Path(os.environ.get('A863_ROOT', '$LANES/arty-4x4'))
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import build
shape, R = sys.argv[1], Path(sys.argv[2])
work = R / 'product-build'
work.mkdir(parents=True, exist_ok=True)
assert shutil.disk_usage(R).free >= 15_000_000_000
flash = build.flash_map(work / 'soc-map', shape)
argv = [sys.executable, '-B', str(ROOT / 'sw/firmware/ctrl/test/ctrl_plat_image.py'), '--config',
        str(ROOT / 'configs' / f'{shape}.yaml'), '--csr-csv', str(work / 'mapped/soc/csr.csv'), '--flash-map',
        str(flash), '--output', str(R / 'product'), '--libc', str(work / 'mapped/runtime/libc.a'),
        '--compiler-runtime', str(work / 'mapped/runtime/libcompiler_rt.a')]
build.run(argv, R / 'product-link.log', cwd=ROOT)
print('PRODUCT', hashlib.sha256((R / 'product/ctrl_app.elf').read_bytes()).hexdigest(), flush=True)
