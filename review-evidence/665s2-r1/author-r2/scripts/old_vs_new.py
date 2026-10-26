#!/usr/bin/env python3
"""The reviewers' probes of the fan-out, reuse and regrade findings, run inside one harness.

Usage: old_vs_new.py HARNESS_DIR OLD_BUILD NEW_BUILD SCRATCH
HARNESS_DIR is a tb/verilator/ctrl_service_budget directory (d58c8e22's or this head's).
OLD_BUILD is a build made at d58c8e22 (basename input keys), NEW_BUILD one made at this head.
Prints one JSON object: what the harness does with each probe (R704-1 probe_graders.py,
R703-1 stale_probe.log and regrade_empty.log).
"""
import contextlib
import hashlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

harness, old_build, new_build, scratch = (Path(a).resolve() for a in sys.argv[1:5])
sys.path.insert(0, str(harness))
import build  # noqa: E402
import grade  # noqa: E402
import scenario  # noqa: E402
import selftest  # noqa: E402

NEW = hasattr(grade, 'fanout_end')
out = {'harness': 'this head' if NEW else 'd58c8e22'}
ch = scenario.CH['aecp']
CTL1 = scenario.CTL1


def response(controller, seq, unsolicited=False):
    f = bytearray(scenario.f.aem_command(scenario.f.Aem(1, controller, 2, 3, seq), 0x10, bytes(8)))
    f[15] = 1
    if unsolicited:
        f[36] |= 0x80
    return bytes(f)


extra = dict(recipients=((CTL1, 0), (CTL1, 1))) if NEW else {}
notify = f'notify:{ch}:0010:0:0' if NEW else f'notify:{ch}'
probe = scenario.Probe('review.notify.if0', 'notification fan-out', 'notify', f'rxc:{ch}',
                       [f'resp:{ch}:41', notify], **extra)
for name, records in (('late_recipient', [(201173, 0, response(2, 0x41)), (401173, 0, response(CTL1, 1, True)),
                                          (1401173, 1, response(CTL1, 2, True))]),
                      ('missing_recipient', [(201173, 0, response(2, 0x41)), (401173, 0, response(CTL1, 1, True))])):
    lines = ['MARK 1000 review.notify.if0', 'RXS 1100 0 70 review.notify.if0', 'RXE 1169', f'RXC 1173 {ch}']
    at = 0
    for cycle, interface, frame in records:
        lines += selftest.tx_record(ch, interface, frame, at, cycle)
        at += 2 + (len(frame) + 3) // 4
    row = selftest.one(selftest.synthetic(lines), probe)
    out[name] = {k: row.get(k) for k in ('status', 'reason', 'end_sys', 'ms', 'within_t_svc')}

# The reuse guard: zero the digests of the inputs outside the checkout, in a copy of each build.json.
for label, source in (('old_build', old_build), ('new_build', new_build)):
    dest = scratch / f'stale-{label}'
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    for name in ('native', 'gateware', 'image', 'runtime', 'budget_config.hpp', 'mbx-variant'):
        if (source / name).exists():
            (dest / name).symlink_to(source / name)
    spec = json.loads((source / 'build.json').read_text())
    planted = [k for k in spec['inputs'] if not k.startswith(('checkout:', 'tree:')) and '/' not in k
               or k.startswith(('build:', 'external:'))]
    results = {}
    for key in planted:
        spec2 = json.loads(json.dumps(spec))
        spec2['inputs'][key] = '0' * 64
        (dest / 'build.json').write_text(json.dumps(spec2))
        try:
            build.reused(dest)
            results[key.split('/')[-1]] = 'accepted'
        except (RuntimeError, OSError) as error:
            results[key.split('/')[-1]] = f'refused: {error}'
    out[f'stale_digest_{label}'] = results

# A regrade of two selected groups from an empty results directory.
empty = scratch / 'empty-regrade'
shutil.rmtree(empty, ignore_errors=True)
empty.mkdir(parents=True)
result = subprocess.run([sys.executable, '-B', str(harness / 'run.py'), '--point', '1x1', '--build-dir', str(new_build),
                         '--regrade', '--out', str(empty), '--groups', 'backlog,backlog-adp',
                         '--record-budget-findings'], capture_output=True, text=True)
out['empty_regrade'] = dict(returncode=result.returncode,
                            stdout=[line for line in result.stdout.splitlines() if not line.startswith('COMMAND')])
print(json.dumps(out, indent=1))
