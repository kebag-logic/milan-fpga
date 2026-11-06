"""Negative probes of the round-6 refusals, on a finished ctrl_split_boot build directory.

usage: refusal_probe.py <tree> <build-dir> <scratch>
  1. split_soc.map_deviations on the boot SoC's real csr.csv: clean, then each way a placement can differ.
  2. boot_soc.build's own export against a map with one register moved: must refuse, in a child process.
  3. ctrl_plat_image.py against a map whose SoC clock is not the shape's: must refuse before compiling.
Exit 1 when a refusal does not fire.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

tree, build, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import split_soc  # noqa: E402

bad = 0


def report(name, ok, detail=''):
    """Print one probe's verdict and count a miss."""
    global bad
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {name}{': ' + detail if detail else ''}")


good = build / 'split-soc/flash-map'
csr = (build / 'soc/csr.csv').read_text()
report('clean csr.csv has no deviation', split_soc.map_deviations(csr, good) == [])
rewrites = {
    'register moved': ('csr_register,spiflash_master_cs,0xf0002810', 'csr_register,spiflash_master_cs,0xf0002814'),
    'timer register moved': ('csr_register,timer0_value,0xf0003010', 'csr_register,timer0_value,0xf0003020'),
    'register absent': ('csr_register,spiflash_master_rxtx,', 'csr_register,spiflash_master_rxtx_gone,'),
    'window moved': ('memory_region,spiflash,0x01000000', 'memory_region,spiflash,0x02000000'),
    'window resized': ('memory_region,spiflash,0x01000000,16777216', 'memory_region,spiflash,0x01000000,8388608'),
    'window absent': ('memory_region,spiflash,', 'memory_region,flash_gone,'),
}
for name, (old, new) in rewrites.items():
    if old not in csr:
        report(name, False, 'anchor absent')
        continue
    found = split_soc.map_deviations(csr.replace(old, new), good)
    report(name, len(found) == 1, str(found)[:150])

shifted = scratch / 'map-shifted'
shutil.rmtree(shifted, ignore_errors=True)
shutil.copytree(good, shifted)
port = json.loads((shifted / 'flash_port.json').read_text())
port['registers']['spiflash_master_cs'] += 4
(shifted / 'flash_port.json').write_text(json.dumps(port))
elf = build / 'image/ctrl_app.elf'
code = ('import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); import boot_soc; '
        'boot_soc.build(Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), 1, Path(sys.argv[5]))')
out = scratch / 'export-shifted'
shutil.rmtree(out, ignore_errors=True)
done = subprocess.run([sys.executable, '-B', '-c', code, str(tree / 'tb/verilator/ctrl_split_boot'), str(out),
                       'endstation_ax7101_1x1_tdm8', str(elf), str(shifted)], cwd=tree, capture_output=True,
                      text=True, check=False)
said = (done.stdout + done.stderr).strip().splitlines()
words = "the boot SoC does not place the flash port's devices as the split SoC does"
report('boot_soc.build refuses a moved register', done.returncode != 0 and words in said[-1], said[-1][:200])

clocked = scratch / 'map-clock'
shutil.rmtree(clocked, ignore_errors=True)
shutil.copytree(good, clocked)
port = json.loads((clocked / 'flash_port.json').read_text())
port['clock_hz'] += 1
(clocked / 'flash_port.json').write_text(json.dumps(port))
runtime = build / 'runtime'
done = subprocess.run([sys.executable, '-B', str(tree / 'sw/firmware/ctrl/test/ctrl_plat_image.py'), '--config',
                       str(tree / 'configs/endstation_ax7101_1x1_tdm8.yaml'), '--csr-csv',
                       str(build / 'soc/csr.csv'), '--flash-map', str(clocked), '--output',
                       str(scratch / 'image-clock'), '--libc', str(runtime / 'libc.a'), '--compiler-runtime',
                       str(runtime / 'libcompiler_rt.a')], cwd=tree, capture_output=True, text=True, check=False,
                      env=os.environ)
said = (done.stdout + done.stderr).strip().splitlines()
report('ctrl_plat_image refuses a clock not the shape\'s', done.returncode == 2 and 'flash map' in said[-1],
       said[-1][:200])
print('misses:', bad)
raise SystemExit(1 if bad else 0)
