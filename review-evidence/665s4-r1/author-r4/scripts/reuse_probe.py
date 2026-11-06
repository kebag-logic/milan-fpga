#!/usr/bin/env python3
"""R738-F2's repeated-output probe, through run.py's real main, at round 3's run.py and at the checkout's.

For each refusal class (a build without its CPU clock, builds that disagree, clocks not the builds', results
misconverted): a success, then that refusal, in one output directory; and a refusal, then a success. Round 3's
main must show the stale table (the finding); the checkout's must leave the refusal alone.
Usage, from the checkout: python3 -B reuse_probe.py ROUND3_RUN_PY
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / 'tb/verilator/nvm_split_target'))
import target_selftest as st

spec = importlib.util.spec_from_file_location('round3_run', sys.argv[1])
round3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(round3)
other = f'CPU 62.5 MHz ({st.OTHER_CPU_HZ:,} Hz), bus 125 MHz ({st.OTHER_SYS_HZ:,} Hz)'
unclocked = dict(sys_hz=st.OTHER_SYS_HZ)
PLANTS = {'a build without its CPU clock': dict(builds={'capture-all': unclocked, 'fixture': unclocked}),
          'builds that disagree': dict(builds={'fixture': dict(cpu_hz=st.CPU_HZ, sys_hz=st.OTHER_SYS_HZ)}),
          "clocks not its builds'": dict(planted=dict(cpu_hz=st.CPU_HZ, sys_hz=st.SYS_HZ)),
          'results misconverted': dict(graded_at=st.CPU_HZ)}
verdicts = {}
for label, module in (('round 3 (ac45db8f)', round3), ('checkout', st.RUN)):
    st.RUN = module
    ok = []
    for plant, kwargs in PLANTS.items():
        with tempfile.TemporaryDirectory() as tmp:
            first = st.main_run(st.OTHER_CPU_HZ, st.OTHER_SYS_HZ, root=Path(tmp))
            again = st.main_run(st.OTHER_CPU_HZ, st.OTHER_SYS_HZ, root=Path(tmp), **kwargs)
            left = sorted(p.name for p in (Path(tmp) / 'results').iterdir())
        status, saved, text, refused = again
        stale = bool(text) and text == first[2]
        print(f'{label}: success rc {first[0]}, then {plant} rc {status}; left {left}; '
              f"table {'the earlier run' + chr(39) + 's, byte-identical' if stale else 'none' if not text else 'new'}; "
              f"results.json {'CPU ' + str(saved.get('cpu_hz')) + ' Hz' if saved else 'none'}")
        ok.append(st.accepted(first, st.OTHER_CPU_HZ, other) and status == 2 and not text and not saved)
    with tempfile.TemporaryDirectory() as tmp:
        first = st.main_run(st.OTHER_CPU_HZ, st.OTHER_SYS_HZ, root=Path(tmp), graded_at=st.CPU_HZ)
        again = st.main_run(st.OTHER_CPU_HZ, st.OTHER_SYS_HZ, root=Path(tmp))
        left = sorted(p.name for p in (Path(tmp) / 'results').iterdir())
    print(f'{label}: refusal rc {first[0]}, then success rc {again[0]}; left {left}')
    ok.append(st.accepted(again, st.OTHER_CPU_HZ, other))
    verdicts[label] = all(ok)
    print(f'{label}: {"SOUND" if verdicts[label] else "STALE OUTPUT"}')
expected = verdicts == {'round 3 (ac45db8f)': False, 'checkout': True}
print('PROBE PASS' if expected else f'PROBE FAIL {verdicts}')
sys.exit(0 if expected else 1)
