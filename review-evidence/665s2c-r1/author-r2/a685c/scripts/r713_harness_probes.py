"""Reviewer mutants of the S2c harness delta, each planted in turn in a disposable copy of the
head's harness, with the self-test run after each; the copy is restored after every probe.
usage: harness_probes.py COPY_ROOT"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
H = root / 'tb/verilator/ctrl_service_budget'
PROBES = [
    ('main reuse refusal removed', 'run.py',
     '        if built_as(spec) != selected(args, shape, n_if):\n',
     '        if False:\n'),
    ('main builds with the default cache, ignoring --fetch-l1', 'run.py',
     'core=builder.Core(args.cpu_regions, args.fetch_l1, args.xip))',
     "core=builder.Core(args.cpu_regions, 'split', args.xip))"),
    ('main never passes the flash image to the model', 'run.py',
     "spec.get('flash_image') or '-'", "'-'"),
    ('build records xip as False', 'build.py',
     "    spec['xip'] = core.xip\n", "    spec['xip'] = False\n"),
    ('split_soc ignores the selected geometry', 'split_soc.py',
     "    scala_args = [*params['scala_args'], *filter(None, [milan_soc.ctrl_cpu_args(geometry)])]\n",
     "    scala_args = [*params['scala_args']]\n"),
    ('fetch_l1_geometry accepts non-power-of-two sets', 'split_soc.py',
     "if not match or int(match.group(1)) & (int(match.group(1)) - 1):",
     "if not match:"),
    ('sim: a refill wait recorded at its first beat', 'sim_main.cpp',
     '(++at.beats == fetch_beats || error)', '(++at.beats >= 1 || error)'),
    ('sim: a refill counts only its first word as code', 'sim_main.cpp',
     'for (unsigned k = 0; k < fetch_beats; ++k) note_code', 'for (unsigned k = 0; k < 1; ++k) note_code'),
]
for label, name, old, new in PROBES:
    f = H / name
    original = f.read_text()
    assert original.count(old) == 1, (label, original.count(old))
    f.write_text(original.replace(old, new))
    try:
        r = subprocess.run([sys.executable, '-B', 'run.py', '--self-test'], cwd=H, capture_output=True, text=True,
                           timeout=600)
        tail = [l for l in r.stdout.splitlines() if l.startswith(('FAIL', 'MUTANT survived', 'self-test:'))]
        print(f"{'KILLED  ' if r.returncode else 'SURVIVED'} {label}: rc={r.returncode} {tail[-1] if tail else ''}")
    finally:
        f.write_text(original)
