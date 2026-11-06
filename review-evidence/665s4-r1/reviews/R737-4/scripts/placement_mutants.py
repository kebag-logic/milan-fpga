#!/usr/bin/env python3
"""placement_mutants.py CHECKOUT BUILD_DIR: each planted defect of a placement control's subject, applied to a disposable
checkout, then --placement-controls on a finished run; a mutant is caught when the run exits non-zero with its words."""
import subprocess, sys
from pathlib import Path
root, build = Path(sys.argv[1]), sys.argv[2]
SOC = 'tb/verilator/ctrl_service_budget/split_soc.py'; BOOT = 'tb/verilator/ctrl_split_boot/boot_soc.py'; RUN = 'tb/verilator/ctrl_split_boot/run.py'
WIN = "if windows != [(port['flash']['base'], port['flash']['size'])]:"
MSG = '''raise RuntimeError(f"the boot SoC does not place the flash port's devices as the split SoC does: {deviations}")'''
CALL = "refuse_deviation(build_dir / 'csr.csv', flash_map)"
M = [
 ('head (no mutant)', None, None, None, None),
 ('register-absent-ignored', SOC, 'if registers.get(name) != want]', 'if name in registers and registers[name] != want]', 'register-absent: WRONG'),
 ('window-base-only', SOC, WIN, "if [w[0] for w in windows] != [port['flash']['base']]:", 'window-resized: WRONG'),
 ('window-size-only', SOC, WIN, "if [w[1] for w in windows] != [port['flash']['size']]:", 'window-moved: WRONG'),
 ('true-map-always-deviates', SOC, "the split SoC's {port['flash']}\")\n    return out", "the split SoC's {port['flash']}\")\n    return out or ['always']", 'true-map: WRONG'),
 ('refusal-words-changed', BOOT, MSG, 'raise RuntimeError(f"the export is wrong: {deviations}")', 'export-refuses: WRONG'),
 ('refusal-names-nothing', BOOT, MSG, '''raise RuntimeError("the boot SoC does not place the flash port's devices as the split SoC does")''', 'export-refuses: WRONG'),
 ('other-failure-first', BOOT, CALL, "raise RuntimeError('an unrelated failure')", 'export-refuses: WRONG'),
 ('plant-inert', RUN, "'guard-removed': 'boot_soc.refuse_deviation = lambda *_: None'", "'guard-removed': 'pass'", 'PLANT guard-removed: ESCAPED'),
]
bad = 0
for name, path, old, new, want in M:
    f = root / path if path else None
    if f:
        text = f.read_text(); assert text.count(old) == 1, (name, text.count(old)); f.write_text(text.replace(old, new))
    d = subprocess.run([sys.executable, '-B', 'tb/verilator/ctrl_split_boot/run.py', '--build-dir', build, '--placement-controls'],
                       cwd=root, capture_output=True, text=True)
    if f: f.write_text(text)
    out = d.stdout + d.stderr
    lines = [l for l in out.splitlines() if 'WRONG' in l or 'ESCAPED' in l or 'placement controls:' in l]
    ok = (d.returncode == 0 and '8 of 8' in out) if want is None else (d.returncode != 0 and want in out)
    bad += not ok
    print(f'{"as expected" if ok else "NOT AS EXPECTED"}: {name}: rc {d.returncode}')
    for l in lines: print('   ', l[:170])
print(f'placement mutants: {len(M)-1} planted, {bad} not as expected')
sys.exit(1 if bad else 0)
