"""Diff the generated files of one service build against the previous round's same build.

Build paths are normalised to `<build>/` on both sides. Text files are diffed
with `diff`; binaries are compared with `cmp`. Output goes to stdout.
"""
from pathlib import Path
import subprocess
import sys

name = sys.argv[1]
old = Path('$VALIDATION_STORAGE/590-a422/native') / name
new = Path('$VALIDATION_STORAGE/590-a430/native') / name
work = Path('$VALIDATION_STORAGE/590-a430/delta') / name
work.mkdir(parents=True, exist_ok=True)
texts = ['software/include/generated/csr.h', 'software/include/generated/soc.h',
         'software/include/generated/mem.h', 'software/include/generated/git.h',
         'software/include/generated/sdram_phy.h', 'gateware/sim.v',
         'generated/endstation_ax7101_1x1_tdm8/adp_shape_defaults.svh',
         'generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh']
binaries = ['software/bios/bios.bin', 'software/bios/bios.elf', 'aem_desc.bin', 'gateware/sim_rom.init',
            'gateware/sim_sram.init', 'gateware/sim_mem.init']
for relative in texts:
    sides = []
    for label, root in (('previous', old), ('head', new)):
        text = (root / relative).read_text().replace(str(root) + '/', '<build>/')
        path = work / (label + '-' + relative.replace('/', '_'))
        path.write_text(text)
        sides.append(str(path))
    print(f'== diff previous round vs this head: {relative} (build paths normalised)', flush=True)
    result = subprocess.run(['diff', *sides], capture_output=True, text=True)
    print(result.stdout, end='')
    print(f'rc={result.returncode}', flush=True)
for relative in binaries:
    result = subprocess.run(['cmp', str(old / relative), str(new / relative)], capture_output=True, text=True)
    print(f'== cmp {relative}', flush=True)
    print(result.stdout.replace(str(old), '<previous>').replace(str(new), '<head>'), end='')
    print(f'rc={result.returncode}', flush=True)
# bios.elf carries DWARF; compare it again with every .debug_* section removed
objcopy = '$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux-objcopy'
stripped = []
for label, root in (('previous', old), ('head', new)):
    path = work / (label + '-bios.nodebug.elf')
    subprocess.run([objcopy, '--strip-debug', str(root / 'software/bios/bios.elf'), str(path)], check=True)
    stripped.append(str(path))
result = subprocess.run(['cmp', *stripped], capture_output=True, text=True)
print('== cmp software/bios/bios.elf after objcopy --strip-debug', flush=True)
print(result.stdout.replace(str(work), '<work>'), end='')
print(f'rc={result.returncode}', flush=True)
