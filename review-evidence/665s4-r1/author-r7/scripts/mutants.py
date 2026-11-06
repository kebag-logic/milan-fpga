#!/usr/bin/env python3
"""Plant each literal defect in a clean clone of the head, one at a time, and require its named check to fail in its
named words. usage: mutants.py <clone> <boot-1x1 build dir> <scratch> <table>. The clone is restored after each.
Exit 0 when every mutant is caught and the clone ends clean."""
import os
import subprocess
import sys
from pathlib import Path

clone, build, scratch, table = (Path(a).resolve() for a in sys.argv[1:5])
scratch.mkdir(parents=True, exist_ok=True)
TOOLS = Path(__file__).resolve().parent
PY = [sys.executable, '-B']
IMAGE = 'sw/firmware/ctrl/test/ctrl_plat_image.py'
BOOT = 'tb/verilator/ctrl_split_boot/boot_soc.py'
SOC = 'tb/verilator/ctrl_service_budget/split_soc.py'
SELFTEST = [*PY, 'sw/firmware/ctrl/test/ctrl_image_selftest.py', '--require-rv32']
PLACEMENT = [*PY, 'tb/verilator/ctrl_split_boot/run.py', '--build-dir', str(build), '--placement-controls']
STOPPED = [sys.executable, '-B', str(TOOLS / 'stopped_probe.py'), str(clone), str(scratch / 'stopped')]
CALL = "    refuse_deviation(build_dir / 'csr.csv', flash_map)\n"
RAISE = ("    if deviations:\n        raise RuntimeError(f\"the boot SoC does not place the flash port's devices as "
         "the split SoC does: {deviations}\")\n")
WINDOW = ("    if windows != [(port['flash']['base'], port['flash']['size'])]:\n"
          "        out.append(f\"the flash window is {windows}, the split SoC's {port['flash']}\")\n")
#: name: (file, anchor, replacement, the check it must fail, the words the check must say, what the check is called)
MUTANTS = {
    'refusal-removed': (IMAGE, "        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n", '',
                        SELFTEST, "AssertionError: ('both archives'", 'ctrl_image_selftest plat'),
    'any-archive-to-all': (IMAGE, 'any(path.exists() for path in archives)', 'all(path.exists() for path in archives)',
                           SELFTEST, "AssertionError: ('the C library alone'", 'ctrl_image_selftest plat'),
    'refused-with-a-map': (IMAGE, 'if flash_map is None and any(', 'if any(', SELFTEST,
                           'AssertionError: REFUSED: no --flash-map', 'ctrl_image_selftest plat'),
    'compile-only-refused': (IMAGE, 'if flash_map is None and any(path.exists() for path in archives):',
                             'if flash_map is None:', STOPPED, 'stopped_at_link False', 'ctrl_runs.stopped_at_link'),
    'guard-call-removed': (BOOT, CALL, '', PLACEMENT, 'PLACEMENT export-refuses: WRONG (export TAKEN)',
                           'run.py --placement-controls'),
    'guard-raise-removed': (BOOT, RAISE, '', PLACEMENT, 'PLACEMENT export-refuses: WRONG (export TAKEN)',
                            'run.py --placement-controls'),
    'deviations-return-empty': (SOC, "    port = json.loads((flash_map / 'flash_port.json').read_text())\n    rows = ",
                                "    return []\n    port = json.loads((flash_map / 'flash_port.json').read_text())\n"
                                "    rows = ", PLACEMENT, 'PLACEMENT register-moved: WRONG',
                                'run.py --placement-controls'),
    'window-unchecked': (SOC, WINDOW, '', PLACEMENT, 'PLACEMENT window-moved: WRONG', 'run.py --placement-controls'),
    'guard-refuses-a-true-map': (BOOT, RAISE, RAISE.replace('if deviations:', 'if True:'),
                                 [*PY, 'tb/verilator/ctrl_split_boot/run.py', '--build-dir',
                                  str(scratch / 'true-map-boot')], 'REFUSED', 'the boot itself'),
}


def git(*argv: str) -> str:
    """git in the clone."""
    return subprocess.run(['git', '-C', str(clone), *argv], capture_output=True, text=True, check=True).stdout


def run(argv: list[str], log: Path) -> tuple[int, str]:
    """One check, its whole output in its log."""
    done = subprocess.run(argv, cwd=clone, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    log.write_text(done.stdout)
    return done.returncode, done.stdout


rows, escaped = [], 0
# the checks must be green with no mutant, or a red one proves nothing
for name, argv in (('head: ctrl_image_selftest', SELFTEST), ('head: placement controls', PLACEMENT),
                   ('head: stopped_at_link', STOPPED)):
    rc, said = run(argv, scratch / f"{name.split(': ')[1].replace(' ', '-')}.log")
    verdict = next((ln for ln in said.splitlines() if 'stopped_at_link' in ln), said.strip().splitlines()[-1])
    print(f'{name}: rc {rc}; {verdict[:140]}', flush=True)
    escaped += rc != 0
    rows.append(f'| {name} (no mutant) | none | | {rc} | `{verdict[:110]}` |')
for name, (path, anchor, new, check, words, called) in MUTANTS.items():
    assert not git('status', '--porcelain', '--untracked-files=all'), 'the clone is not clean'
    text = (clone / path).read_text()
    assert text.count(anchor) == 1, (name, text.count(anchor))
    (clone / path).write_text(text.replace(anchor, new))
    rc, said = run(check, scratch / f'{name}.log')
    git('checkout', '--', path)
    caught = rc != 0 and words in said
    escaped += not caught
    line = next((ln.strip() for ln in said.splitlines() if words in ln), '')
    print(f'{name}: {"CAUGHT" if caught else "ESCAPED"}, rc {rc}, by {called}: {line[:150]}', flush=True)
    rows.append(f'| {name} | `{path}` | {called} | {rc} | `{line[:110]}` |')
clean = not git('status', '--porcelain', '--untracked-files=all')
table.write_text('| Mutant | File | Caught by | rc | Failing words |\n|---|---|---|---:|---|\n' + '\n'.join(rows) + '\n')
print(f'mutants: {len(MUTANTS)} planted, {escaped} escaped; clone clean after: {clean}')
sys.exit(1 if escaped or not clean else 0)
