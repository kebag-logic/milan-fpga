"""Every shipping product ELF (the split placement's ctrl_app.elf of each shipping configuration) built from a clean
export of each head, as round 9's product recipe builds it: the shape's SoC map and flash port, then the platform
image. Prints each ELF's SHA256 by head and shape, and exits 1 unless each shape's are identical across heads."""
import hashlib, json, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parent
W = Path('$SOURCE')
HEADS = sys.argv[1:3]
SHAPES = ('endstation_arty_split', 'endstation_ax7101_8x8', 'endstation_ax7101_1x1_tdm8')
PY = '$TOOLCHAIN/venv/bin/python3'
CODE = '''
import sys, hashlib
from pathlib import Path
root, work, shape = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import build
flash = build.flash_map(work / 'soc-map', shape)
argv = [sys.executable, '-B', str(root / 'sw/firmware/ctrl/test/ctrl_plat_image.py'), '--config',
        str(root / 'configs' / f'{shape}.yaml'), '--csr-csv', str(work / 'mapped/soc/csr.csv'), '--flash-map',
        str(flash), '--output', str(work / 'image'), '--libc', str(work / 'mapped/runtime/libc.a'),
        '--compiler-runtime', str(work / 'mapped/runtime/libcompiler_rt.a')]
build.run(argv, work / 'image-link.log', cwd=root)
print(hashlib.sha256((work / 'image/ctrl_app.elf').read_bytes()).hexdigest())
'''


def export(sha):
    """A clone of the head with git metadata, its submodules at their pins from the local checkouts."""
    tree = R / 'clones' / sha[:12]
    if not tree.exists():
        subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', str(W), str(tree)], check=True)
        subprocess.run(['git', 'checkout', '-q', sha], cwd=tree, check=True)
        names = subprocess.check_output(['git', 'config', '-f', '.gitmodules', '--get-regexp', r'submodule\..*\.path'],
                                        cwd=tree, text=True).split('\n')
        for line in filter(None, names):
            key, path = line.split()
            name = key[len('submodule.'):-len('.path')]
            subprocess.run(['git', '-c', 'protocol.file.allow=always', '-c', f'submodule.{name}.url={W / path}',
                            'submodule', 'update', '--init', '--quiet', path], cwd=tree, check=True)
            subprocess.run(['git', 'config', f'submodule.{name}.url', str(W / path)], cwd=tree, check=True)
    return tree


rows = {}
for sha in HEADS:
    tree = export(sha)
    for shape in SHAPES:
        work = R / 'build2' / sha[:12] / shape
        work.mkdir(parents=True, exist_ok=True)
        with (work / 'product.log').open('w') as log:
            out = subprocess.run([PY, '-B', '-c', CODE, str(tree), str(work), shape], cwd=tree, stdout=subprocess.PIPE,
                                 stderr=log, text=True)
        digest = out.stdout.strip().splitlines()[-1] if out.returncode == 0 and out.stdout.strip() else f'FAILED rc={out.returncode}'
        rows.setdefault(shape, {})[sha] = digest
        print(shape, sha[:12], digest, flush=True)
same = all(len(set(v.values())) == 1 and not next(iter(v.values())).startswith('FAILED') for v in rows.values())
(R / 'product-identity.json').write_text(json.dumps(dict(heads=HEADS, elf_sha256=rows, identical=same), indent=1) + '\n')
print('RESULT', 'IDENTICAL' if same else 'DIFFER OR FAILED')
sys.exit(0 if same else 1)
