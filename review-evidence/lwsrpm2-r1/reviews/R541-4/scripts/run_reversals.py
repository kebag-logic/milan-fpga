# SPDX-License-Identifier: Apache-2.0
"""Replay a fixed published sample plus two independently selected faults."""
import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--jobs', type=int, default=2)
p.add_argument('--worker', choices=['OFF', 'ON'])
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
selected = {
    'flush-retry', 'replacement-order', 'receive-stop', 'policy-mask', 'no-policy-reservation',
    'changed-in-only', 'stream-list-boundary', 'changed-value-rollback',
    'registrar-rollback', 'applicant-rollback', 'leave-timer-retry',
    'receive-map-error', 'reservation-atomicity', 'poll-replay', 'commit-replay',
    'queue-teardown', 'zero-attribute-length', 'changed-value-propagation',
    'replay-error-retention', 'callback-order',
    'application-decode-error', 'stream-increment-overflow', 'domain-priority-range',
    'vlan-range', 'mac-increment-overflow', 'unknown-event-extension',
    'current-version-extension', 'propagation-retention', 'propagation-order',
    'registrar-recovery-indication', 'committed-local-leaveall',
    'omitted-leaveall-event', 'reserved-leaveall-event', 'listener-subtype',
    'leaveall-upper-bound', 'reclaim-leaving-observer', 'milan-redeclare-scope',
    'milan-transmitted-leaveall-scope', 'received-leaveall-restart',
    'milan-delayed-in-leave', 'milan-restarted-lv-deadline', 'leaveall-scope',
}
if a.worker:
    spec = importlib.util.spec_from_file_location('reviewed_reversals', source / 'tests/check_reversals.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert len(module.CASES) == 80
    module.CASES = [case for case in module.CASES if case[0] in selected]
    assert len(module.CASES) == len(selected)
    module.CASES += [
        ('own-short-value-restore', module.MAD,
         'memcpy(ai->attr_val, previous_value, sizeof(previous_value));',
         'memcpy(ai->attr_val, previous_value, 8);', 'unit'),
        ('own-last-destination-lost', module.MAD,
         'p < priv_of(app)->n_ports && p < 32u;',
         'p + 1u < priv_of(app)->n_ports && p < 32u;', 'unit'),
    ]
    module.CASES += [('own-flush-two-tick-delay', module.MAD, 'ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 1u);', 'ai->reg = MRP_REG_STATE_LV;\n            shlan_timer_arm(&ai->leave_timer, 2u);', 'unit')]
    module.REQUIRED_FAILURES.update({
        'own-flush-two-tick-delay': ['flush_allocation_failures_retry_withdrawal_on_the_next_tick'],
        'own-short-value-restore': ['changed_value_allocation_failure_preserves_retry'],
        'own-last-destination-lost': ['changed_values_after_received_leaveall_are_indicated_and_propagated'],
    })
    sys.argv = ['check_reversals.py', '--work-dir', str(packet / 'scratch' / ('reversals-' + a.worker)), '--prefix', str(packet / 'scratch/deps'), '--milan', a.worker]
    raise SystemExit(module.main())

def worker(profile):
    env = os.environ | {'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(packet / 'scratch')}
    cmd = [sys.executable, __file__, '--source', str(source), '--packet', str(packet), '--worker', profile]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=540)
    def clean(text):
        return text.replace(str(source), '$SOURCE').replace(str(packet), '$PACKET')
    dest = packet / 'receipts' / ('reversals-' + profile)
    dest.mkdir(exist_ok=True)
    (dest / 'campaign.log').write_text(clean(r.stdout + r.stderr))
    (dest / 'campaign.rc').write_text(str(r.returncode) + '\n')
    for f in (packet / 'scratch' / ('reversals-' + profile)).glob('*'):
        if f.is_file() and f.suffix in ('.log', '.json'):
            (dest / f.name).write_text(clean(f.read_text()))
    records = json.loads((dest / 'commands.json').read_text())
    for entry in records:
        (dest / (entry['label'] + '.rc')).write_text(str(entry['rc']) + '\n')
    print(profile, 'rc', r.returncode, r.stdout[-700:], r.stderr[-500:], flush=True)
    return r.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs, 2)) as pool:
    result = list(pool.map(worker, ['OFF', 'ON']))
raise SystemExit(any(result))
