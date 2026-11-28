"""Byte identity of every existing image's inputs at base and head: the builder's outputs for each existing config
and the linked product ELF of each existing split config. usage: identity.py <side: base|head> <outdir>"""
import hashlib, json, os, subprocess, sys
from pathlib import Path
side, out = sys.argv[1], Path(sys.argv[2]).resolve()
root = Path({'base': '$VALIDATION_STORAGE/arty4x4-a863/base', 'head': '$LANES/arty-4x4'}[side])
tools = Path(__file__).resolve().parent
CONFIGS = ('endstation_arty_4x4', 'endstation_arty_8ch', 'endstation_arty_current', 'endstation_arty_split',
           'endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')
PRODUCTS = ('endstation_arty_split', 'endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')
out.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, A863_ROOT=str(root))
digests = {}
for c in CONFIGS:
    o = out / 'builder' / c
    subprocess.run([sys.executable, '-B', str(root / 'sw/builder/endstation_builder.py'), str(root / 'configs' / f'{c}.yaml'),
                    '-o', str(o)], cwd=root, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for p in sorted(o.rglob('*')):
        if p.is_file():
            digests[f'builder/{p.relative_to(o.parent)}'] = hashlib.sha256(p.read_bytes()).hexdigest()
for c in PRODUCTS:
    o = out / 'product' / c
    with (out / f'product-{c}.log').open('w') as log:
        subprocess.run([sys.executable, '-B', str(tools / 'product.py'), c, str(o)], cwd=root, env=env, check=True,
                       stdout=log, stderr=subprocess.STDOUT)
    elf = o / 'product/ctrl_app.elf'
    digests[f'product/{c}/ctrl_app.elf'] = hashlib.sha256(elf.read_bytes()).hexdigest()
    digests[f'product/{c}/size.json'] = hashlib.sha256((o / 'product/size.json').read_bytes()).hexdigest()
(out / 'digests.json').write_text(json.dumps(digests, indent=1, sort_keys=True) + '\n')
print('DIGESTS', side, len(digests))
