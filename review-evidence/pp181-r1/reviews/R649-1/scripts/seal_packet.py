#!/usr/bin/env python3
"""Check receipt outcomes and write a sha256sum-format publication inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import re

p = argparse.ArgumentParser()
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
root = a.packet.resolve()
r = root / 'receipts'
summary = {}
for name in ['router', 'notify', 'docs', 'top-build', 'top-notify', 'top-aecp-dispatch',
             'top-spacing', 'top-hazards', 'top-budget']:
    rc = int((r / (name + '.rc')).read_text())
    assert rc == 0, (name, rc)
    summary[name] = {'rc': rc}
for group, names in [('queue', ['base', 'control', 'push-unseen', 'pop-occupied', 'pop-offbyone']),
                     ('router', ['base', 'control', 'base-pointer', 'presented-retained', 'ignore-ack'])]:
    for name in names:
        label = group + '-' + name
        rc = int((r / (label + '.rc')).read_text())
        assert (rc == 0) == (name in ['base', 'control']), (label, rc)
        if group == 'queue':
            assert int((r / (label + '-build.rc')).read_text()) == 0
            text = (r / (label + '.log')).read_text()
            count = re.search(r'queue probe: (\d+) failures; (\d+) delivered jobs', text)
            assert count
            assert (int(count[1]) == 0) == (rc == 0)
            summary[label] = {'rc': rc, 'failures': int(count[1]), 'delivered_jobs': int(count[2]), 'build_succeeded': True}
        else:
            text = (r / (label + '-build.log')).read_text()
            assert './obj_dir/Vevtr_sim\n' in text
            count = re.search(r'81 checks: (\d+) PASS, (\d+) FAIL', text)
            assert count
            assert (int(count[2]) == 0) == (rc == 0)
            summary[label] = {'rc': rc, 'checks': 81, 'failures': int(count[2]), 'build_succeeded': True}
assert (r / 'queue-base.log').read_bytes() == (r / 'queue-control.log').read_bytes()
summary['queue_base_head_trace_identical'] = True
report = (root / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R649] NEGATIVE - exact head 42eb9aef3642f6d98058fe634a70f6a9c749cd25'
assert report.splitlines()[-1] == 'R649-1 FINISHED'
assert 'SKELETON' not in report
summary['report_complete'] = True
(r / 'execution-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
paths = [root / 'REPORT.md']
for directory in ('receipts', 'scripts'):
    paths += [f for f in (root / directory).rglob('*') if f.is_file() and '__pycache__' not in f.parts]
lines = [hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + f.relative_to(root).as_posix() for f in sorted(paths)]
(root / 'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print(json.dumps(summary, indent=2))
print('Manifest files:', len(paths))
