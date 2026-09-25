"""Compile the generated product netlist with an edge-scheduled runner."""
import json
from pathlib import Path
import shlex
import subprocess

root = Path('$LANES/559-capture-copy')
build = Path('$VALIDATION_STORAGE/559-a307-product-preflight/endstation_ax7101_8x8')
spec = json.loads((build / 'sources.json').read_text())
source = Path(__file__).with_name('capture_sim_main.cpp')
argv = ['verilator', '--cc', '--exe', '--build', '-j', '8', '-Wno-fatal',
        '-Wno-BLKANDNBLK', '-Wno-WIDTH', '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE',
        '--top-module', 'sim', '--Mdir', str(build / 'native'), '-O3',
        '--output-split', '5000', '--output-split-cfuncs', '500',
        '-CFLAGS', '-O3 -I' + str(root / 'tb/common'),
        *['-I' + str(i) for i in spec['includes']], *spec['sources'], str(source)]
print('command:', shlex.join(argv), flush=True)
subprocess.run(argv, cwd=build / 'gateware', check=True, timeout=3600)
