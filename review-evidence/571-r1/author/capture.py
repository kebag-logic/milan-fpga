"""Capture generated artifacts and elaboration statistics for issue #571."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('$LANES/571-pp-unit-counts')
WORK = Path('/tmp/571-a371')
sys.path.insert(0, str(ROOT / 'sw/builder'))
import endstation_builder as builder

phase = sys.argv[1]
dest = WORK / phase
dest.mkdir(parents=True, exist_ok=True)
manifest = {}
shapes = {}
for cfg in sorted((ROOT / 'configs').glob('endstation_*.yaml')):
    result = builder.build(str(cfg), str(dest / 'artifacts'))
    name = result['cfg']['name']
    directory = dest / 'artifacts' / name
    counts = result['overlay']['descriptor_counts']
    assert all(counts[k] == 1 for k in ('AUDIO_UNIT', 'CLOCK_DOMAIN', 'CONTROL')), counts
    (directory / 'sweep_opts.sh').write_text(result['sweep_opts'])
    (directory / 'interface_params.json').write_text(json.dumps(result['interface_params'], sort_keys=True, indent=2) + '\n')
    subprocess.run([sys.executable, str(ROOT / 'avdecc/gen_aemi_image.py'),
                    '--overlay', str(directory / 'aem_overlay.json'),
                    '-o', str(directory / 'aem_desc.bin'),
                    '-m', str(directory / 'aem_desc.map')], check=True, capture_output=True)
    manifest[name] = {
        p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in sorted(directory.iterdir()) if p.is_file()
    }
    shapes[name] = {
        'N_STREAM_IN_P': counts['STREAM_INPUT'],
        'N_STREAM_OUT_P': counts['STREAM_OUTPUT'],
        'N_SPORT_IN_P': counts['STREAM_PORT_INPUT'],
        'N_SPORT_OUT_P': counts['STREAM_PORT_OUTPUT'],
        'N_AUDIO_UNIT_P': counts['AUDIO_UNIT'],
        'N_CLK_DOM_P': counts['CLOCK_DOMAIN'],
        'DESC_NAME_ENTRIES_P': int(re.search(r'AEM_NAME_ENTRIES_C\s*=\s*(\d+)', result['adp_shape_svh'])[1]),
    }
    if phase != 'base':
        shapes[name]['N_CONTROL_P'] = counts['CONTROL']
    print(name, counts['AUDIO_UNIT'], counts['CLOCK_DOMAIN'], counts['CONTROL'], flush=True)
(dest / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(dest / 'shapes.json').write_text(json.dumps(shapes, indent=2) + '\n')
if '--elaborate' in sys.argv:
    source_lines = subprocess.check_output(['bash', str(ROOT / 'syn/yosys/run.sh'), '--emit', 'KL_pp_shadow'], text=True).splitlines()
    sources = [line.removeprefix('src=') for line in source_lines if line.startswith('src=')]
    assert sources and all(Path(p).is_file() for p in sources), sources
    for name in ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8'):
        out = dest / name
        out.mkdir(exist_ok=True)
        argv = ['verilator', '--cc', '--stats', '-Wno-fatal', '--top-module', 'KL_pp_shadow',
                '--Mdir', str(out), *[f'-G{k}={v}' for k, v in shapes[name].items()], *sources]
        (out / 'argv.json').write_text(json.dumps(argv, indent=2) + '\n')
        with (out / 'elaborate.log').open('w') as log:
            subprocess.run(argv, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=900)
        print('elaborated', name, flush=True)
