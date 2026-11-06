#!/usr/bin/env python3
"""own_mutants.py CHECKOUT BOOT: the reviewer's probes of the refusal and the placement controls.

Real deviations: the boot SoC's own placement shifted, on the true map, through run.py's exported(plant=...). Mutants:
one literal source edit each, in CHECKOUT, the control re-run, the edit reverted. CHECKOUT must be a disposable clone."""
import importlib.util, subprocess, sys
from pathlib import Path

ck, boot = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ck / 'tb/verilator/ctrl_split_boot'))
spec = importlib.util.spec_from_file_location('split_boot_run', ck / 'tb/verilator/ctrl_split_boot/run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
POINT = ('endstation_ax7101_1x1_tdm8', 1)


def shifted(key: str, by: int) -> str:
    """A plant statement: the SoC placed with one address moved, the image and the map unchanged."""
    return (f"_f = boot_soc.split_soc.fixture_addresses; "
            f"boot_soc.split_soc.fixture_addresses = lambda m: {{**_f(m), {key!r}: _f(m)[{key!r}] + {by}}}")


def real(name: str, plant: str) -> str:
    """How the export ends on the true map under `plant`."""
    try:
        run.exported(boot, name, POINT, boot / 'image/ctrl_app.elf', boot / 'split-soc/flash-map', plant)
    except RuntimeError:
        said = (boot / f'{name}.log').read_text().strip().rsplit('\n', 1)[-1]
        return ('REFUSED ' if run.DEVIATES in said else 'OTHER ') + said[:230]
    return 'TAKEN'


def edit(path: str, old: str, new: str) -> tuple[Path, str]:
    """One literal edit; the file and its original text."""
    file = ck / path
    text = file.read_text()
    assert text.count(old) == 1, (path, old, text.count(old))
    file.write_text(text.replace(old, new))
    return file, text


def control(*argv: str) -> tuple[int, str]:
    """A control's exit status and its last line."""
    done = subprocess.run([sys.executable, '-B', *argv], cwd=ck, capture_output=True, text=True, check=False)
    return done.returncode, (done.stdout + done.stderr).strip().rsplit('\n', 1)[-1][:200]


PLACE = ('tb/verilator/ctrl_split_boot/run.py', '--build-dir', str(boot), '--placement-controls')
SELF = ('sw/firmware/ctrl/test/ctrl_image_selftest.py', '--require-rv32', '--out', str(boot / 'mut-selftest'))
SPLIT = 'tb/verilator/ctrl_service_budget/split_soc.py'
PLAT = 'sw/firmware/ctrl/test/ctrl_plat_image.py'
CALL = '        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n'
LINK = '        libraries = [args.libc.resolve(), args.compiler_runtime.resolve()]\n'

print('REAL timer0 +0x800:', real('real-timer0', shifted('timer0', 0x800)))
print('REAL spiflash +0x800:', real('real-spiflash', shifted('spiflash', 0x800)))
print('REAL flash window +0x1000:', real('real-flash', shifted('flash', 0x1000)))
print('REAL flash size / 2:', real('real-size', shifted('flash_size', -0x800000)))

MUTANTS = (
    ('deviations-ignore-timer', SPLIT, "for name, want in port['registers'].items() if registers.get(name) != want]",
     "for name, want in port['registers'].items() if name.startswith('spiflash') and registers.get(name) != want]",
     PLACE),
    ('deviations-only-the-moved-register', SPLIT,
     "for name, want in port['registers'].items() if registers.get(name) != want]",
     "for name, want in port['registers'].items() if name in ('spiflash_master_cs', 'spiflash_absent') and "
     "registers.get(name) != want]", PLACE),
    ('window-base-only', SPLIT, "if windows != [(port['flash']['base'], port['flash']['size'])]:",
     "if [w[0] for w in windows] != [port['flash']['base']]:", PLACE),
    ('refusal-libc-only', PLAT, 'any(path.exists() for path in archives)', 'archives[0].exists()', SELF),
)
for name, path, old, new, argv in MUTANTS:
    file, text = edit(path, old, new)
    try:
        rc, said = control(*argv)
        extra = ''
        if name.startswith('deviations'):
            extra = f"; real timer0 +0x800: {real('real-timer0-m', shifted('timer0', 0x800)).split(' ', 1)[0]}"
        print(f'MUTANT {name}: control rc {rc}: {said}{extra}')
    finally:
        file.write_text(text)

file = ck / PLAT
text = file.read_text()
assert text.count(CALL) == 1 and text.count(LINK) == 1
file.write_text(text.replace(CALL, '').replace(LINK, CALL + LINK))
try:
    rc, said = control(*SELF)
    print(f'MUTANT refusal-after-the-compile: control rc {rc}: {said}')
finally:
    file.write_text(text)
print('tree status lines:', subprocess.run(['git', 'status', '--porcelain'], cwd=ck, capture_output=True, text=True).stdout.count('\n'))
