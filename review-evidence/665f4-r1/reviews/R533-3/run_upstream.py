#!/usr/bin/env python3
"""Public note-4/5 topic, unchanged production, both profiles and three plants."""
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--prefix', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--jobs', type=int, default=16)
a = p.parse_args()
out = a.packet.resolve() / 'upstream'
out.mkdir(exist_ok=True)
scratch = a.packet.resolve() / 'scratch' / 'upstream'
scratch.mkdir(exist_ok=True)
src = scratch / 'source'
shutil.copytree(a.source, src, dirs_exist_ok=True)
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = str(a.prefix.resolve() / 'lib') + ':' + env.get('LD_LIBRARY_PATH', '')
env['PYTHONDONTWRITEBYTECODE'] = '1'
records = []
def run(name, command, expected=0, needles=()):
    r = subprocess.run(list(map(str, command)), cwd=src, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, timeout=540)
    (out / (name + '.log')).write_text(r.stdout)
    (out / (name + '.rc')).write_text(str(r.returncode) + '\n')
    ok = (r.returncode == 0 if expected == 0 else r.returncode != 0) and all(n in r.stdout for n in needles)
    records.append({'name': name, 'command': list(map(str, command)), 'rc': r.returncode, 'accepted': ok})
    (out / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
    print(name, 'rc=', r.returncode, 'accepted=', ok, flush=True)
    if not ok:
        raise SystemExit(1)

for profile in ('OFF', 'ON'):
    b = scratch / ('build-' + profile)
    run(profile + '-configure', ['cmake', '-S', src, '-B', b, '-DCMAKE_BUILD_TYPE=Release',
                                '-DLWSRP_MILAN=' + profile, '-DCMAKE_PREFIX_PATH=' + str(a.prefix.resolve())])
    run(profile + '-build', ['make', '-j' + str(a.jobs), '-C', b])
    run(profile + '-unit', [b / 'unit_tests'], needles=('passes',))
    env['SHLAN_LIBRARY'] = str(b / 'libshlan.so')
    run(profile + '-behave', ['behave', 'tests/features', '--no-capture'], needles=('3 scenarios passed',))

target = src / 'src/core/mrp_mad.c'
original = target.read_text()
plants = [
    ('note4-VO-VP', 'if ((p2p && ev == MRP_EVENT_RJOININ &&',
     'if ((false && p2p && ev == MRP_EVENT_RJOININ &&',
     ('applicant_receive_conditions_follow_link_mode', 'pending_applicant_joinin_obeys_note_four')),
    ('note4-VP', 'ai->appl == MRP_APPL_STATE_VO || ai->appl == MRP_APPL_STATE_VP',
     'ai->appl == MRP_APPL_STATE_VO', ('pending_applicant_joinin_obeys_note_four',)),
    ('note5-shared', '(!p2p && ev == MRP_EVENT_RIN)',
     '(false && !p2p && ev == MRP_EVENT_RIN)', ('applicant_receive_conditions_follow_link_mode',)),
]
b = scratch / 'build-ON'
for name, old, new, needles in plants:
    assert original.count(old) == 1, name
    target.write_text(original.replace(old, new))
    try:
        run(name + '-build', ['make', '-j' + str(a.jobs), '-C', b])
        run(name + '-unit', [b / 'unit_tests'], expected=1, needles=('Failure:', *needles))
    finally:
        target.write_text(original)
run('restored-build', ['make', '-j' + str(a.jobs), '-C', b])
run('restored-unit', [b / 'unit_tests'], needles=('passes',))
print('RESULT: PASS')
