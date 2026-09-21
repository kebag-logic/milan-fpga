"""Run the independent router/S4 probe and its two one-sided-gating controls.

Set EVIDENCE_ROOT to the public evidence checkout, REVIEW_OUT to private
scratch, and use taskset -c 64-79 python3 -B reproduce_router.py.
"""
import json
import os
import pathlib
import resource
import subprocess

resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
evidence = pathlib.Path(os.environ['EVIDENCE_ROOT']).resolve()
out = pathlib.Path(os.environ['REVIEW_OUT']).resolve()
out.mkdir(parents=True, exist_ok=True)
rows = []
for mode in range(3):
    obj = out / f'router-probe-{mode}'
    cmd = ['verilator', '--binary', '--timing', '-Wno-fatal', '--top-module',
           'router_probe', f'-GMODE={mode}', '--Mdir', str(obj), '-j', '8',
           str(pathlib.Path(__file__).with_name('router_probe.sv').resolve()),
           str(evidence / 'protocol-processor/hdl/packet_engine/KL_pp_event_router.sv'),
           str(evidence / 'design-evidence/500-materialization/proposal-evidence/prototype/KL_pp_acmp_lsn_admit.proto.sv')]
    build = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (out / f'build-{mode}.log').write_text(build.stdout)
    if build.returncode:
        raise SystemExit(build.returncode)
    run = subprocess.run([str(obj / 'Vrouter_probe')], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True)
    (out / f'run-{mode}.log').write_text(run.stdout)
    correct = run.returncode == 0 if mode == 0 else (
        run.returncode != 0 and 'pop/take disagreement' in run.stdout)
    rows.append({'mode': mode, 'exit': run.returncode, 'expected': correct})
    print(rows[-1], flush=True)
(out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
raise SystemExit(any(not row['expected'] for row in rows))
