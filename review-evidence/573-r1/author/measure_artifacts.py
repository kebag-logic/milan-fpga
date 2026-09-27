"""Generate all assigned artifacts in disposable scratch and retain hashes only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path('$LANES/573-builder-refusals')
sys.path.insert(0, str(ROOT / 'sw/builder'))
import endstation_builder as builder


def measure():
    rows = []
    names = subprocess.check_output(
        ['git', 'ls-files', 'configs/endstation_*.yaml'], cwd=ROOT, text=True).splitlines()
    assert len(names) == 5, names
    for name in names:
        with tempfile.TemporaryDirectory(prefix='shipping-artifacts-') as scratch:
            directory = Path(scratch)
            result = builder.build(str(ROOT / name), str(directory / 'builder'))
            config = Path(name).stem
            built = directory / 'builder' / config
            overlay = built / 'aem_overlay.json'
            store = directory / 'store'
            image = directory / 'image'
            image.mkdir()
            commands = [
                ['python3', str(ROOT / 'avdecc/gen_aem_store.py'), '--overlay', str(overlay),
                 '--out-dir', str(store)],
                ['python3', str(ROOT / 'avdecc/gen_aemi_image.py'), '--overlay', str(overlay),
                 '-o', str(image / 'aem_desc.bin'), '-m', str(image / 'aem_desc.map'),
                 '--json', str(image / 'aem_desc.json')],
            ]
            for command in commands:
                subprocess.run(command, check=True, cwd=ROOT, capture_output=True, timeout=300)
            artifacts = {str(p.relative_to(built)): p.read_bytes() for p in built.rglob('*') if p.is_file()}
            artifacts = {'builder/' + key: data for key, data in artifacts.items()}
            artifacts['builder/gen/adp_shape_defaults.svh'] = Path(result['paths']['cfg_adp_shape_svh']).read_bytes()
            artifacts['builder/sweep_opts.generated.sh'] = result['sweep_opts'].encode()
            for label, location in [('store', store), ('image', image)]:
                artifacts.update({label + '/' + str(p.relative_to(location)): p.read_bytes()
                                  for p in location.rglob('*') if p.is_file()})
            for label, data in sorted(artifacts.items()):
                rows.append(dict(configuration=config, artifact=label, bytes=len(data),
                                 sha256=hashlib.sha256(data).hexdigest()))
            print(f'{config}: {len(artifacts)} artifacts accepted')
    return rows


if __name__ == '__main__':
    destination = Path(sys.argv[1])
    rows = measure()
    destination.write_text(json.dumps(rows, indent=2) + '\n')
    print(f'{len(rows)} artifact hashes written to {destination.name}')
