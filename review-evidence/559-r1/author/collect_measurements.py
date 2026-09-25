import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

root = Path('$LANES/559-capture-copy')
out = Path(__file__).parent
harness = root / 'tb/verilator/nvm_capture_cpu'
module_spec = importlib.util.spec_from_file_location('capture_runner', harness / 'run.py')
runner = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(runner)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

receipt = {
    'date': '2026-09-25',
    'base': 'a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4',
    'compiler': 'riscv32-linux-gcc 14.3.0, RV32I, ILP32, -Os',
    'soc_component_revisions': json.loads((out / 'environment-revisions.json').read_text()),
    'cpu_generator_revision': '235753e24f2d960e49a0852205bae1400bf22c19',
    'cpu_generator_note': 'Existing product patches retained; generated netlist hashes below identify their output.',
    'simulator': 'Verilator 5.052',
    'network': 'disabled; offline dependency resolution',
    'python_hash_seed': 'Unset in measurements. A seed-0 8x8 build produced byte-identical CPU, BIOS, firmware and shape inputs; SoC RTL differs only in date comments and build path. Both measured CPU netlists are identical after normalizing only the top module name.',
    'timer': '100 MHz system downcounter, before ARM through successful ATTEST',
    'harness_sha256': {p.name: digest(p) for p in sorted(harness.iterdir())
                       if p.suffix in ('.py', '.cpp')},
    'product_firmware_sha256': digest(root / 'sw/firmware/milan_baremetal/milan_baremetal.c'),
    'measurements': [],
}
for name in ('8x8', '1x1'):
    build = Path('$VALIDATION_STORAGE/559-a307-final-' + name)
    assert (out / ('final-' + name + '.rc')).read_text().strip() == '0'
    spec = json.loads((build / 'sources.json').read_text())
    # Reapply the final source's complete grader, including the shape census.
    runner._grade(build, spec, 0)
    result = json.loads((build / 'measurement.json').read_text())
    result['command'] = ('python3 tb/verilator/nvm_capture_cpu/run.py --shape '
                         + spec['shape'] + ' --captures 16 --build-dir /tmp/nvm-capture-' + name)
    cpu_source = [Path(p) for p in spec['sources'] if Path(p).name.startswith('VexiiRiscvLitex_')]
    assert len(cpu_source) == 1
    result['cpu_netlist_sha256'] = digest(cpu_source[0])
    result['instrumented_firmware_sha256'] = digest(build / 'measurement_firmware/milan_baremetal.c')
    result['bios_sha256'] = digest(build / 'software/bios/bios.bin')
    receipt['measurements'].append(result)
    shutil.copyfile(build / 'capture.log', out / ('final-' + name + '-uart.log'))
    shutil.copyfile(build / 'measurement.json', out / ('final-' + name + '-measurement.json'))

# Keep every raw row together on one line so a reviewer can compare captures.
text = json.dumps(receipt, indent=2)
for result in receipt['measurements']:
    for row in result['rows']:
        expanded = json.dumps(row, indent=2).replace('\n', '\n        ')
        text = text.replace(expanded, json.dumps(row))
(harness / 'measurements.json').write_text(text + '\n')
(out / 'measurements.json').write_text(text + '\n')
