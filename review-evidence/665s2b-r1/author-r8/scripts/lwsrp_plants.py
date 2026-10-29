#!/usr/bin/env python3
"""The lwSRP donor's planted defects: each copies the donor checkout, makes ONE substitution (exactly once), builds
and runs lwSRP's unit runner (doc/tester.md), and requires the named test among its failures.
usage: lwsrp_plants.py DONOR_CHECKOUT SCRATCH"""
import concurrent.futures, os, shutil, subprocess, sys
from pathlib import Path
SRC, ROOT = Path(sys.argv[1]), Path(sys.argv[2])
P = '$VALIDATION_STORAGE/665s2b-a683j/cgreen/prefix'
ENV = dict(os.environ, CGREEN_PREFIX=P, CMAKE_PREFIX_PATH=P, LD_LIBRARY_PATH=f'{P}/lib', CPATH=f'{P}/include',
           LIBRARY_PATH=f'{P}/lib')
PLANTS = [
    ('leave-timer-unnoted', 'src/core/mrp_mad.c', '    note_states(&priv_of(a->app)->ports[a->port_id], a->ai);\n', '',
     'registration_ended_by_the_leave_timer_is_reclaimed_after_an_earlier_walk'),
    ('event-unnoted', 'src/core/mrp_mad.c', '        return r; /* The restored states were marked when they were reached. */\n    }\n    note_states(ps, ai);\n',
     '        return r; /* The restored states were marked when they were reached. */\n    }\n',
     'leaving_observer_is_retained_until_its_pending_transmission'),
    ('creation-unnoted', 'src/core/mrp_mad.c', '    ps->attrs     = a;\n    note_states(ps, a);\n', '    ps->attrs     = a;\n',
     'refused_replacement_leaves_its_new_instance_reclaimable'),
    ('walk-always-skipped', 'src/core/mrp_mad.c', '    if (!ps->reclaim_due) {\n', '    if (true) {\n',
     'uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed'),
    ('reclaimable-leaving-observer', 'src/core/mrp_mad.c', 'a->appl == MRP_APPL_STATE_AO || a->appl == MRP_APPL_STATE_QO);',
     'a->appl == MRP_APPL_STATE_AO || a->appl == MRP_APPL_STATE_QO || a->appl == MRP_APPL_STATE_LO);',
     'leaving_observer_is_retained_until_its_pending_transmission'),
    ('delivery-not-cleared', 'src/core/mrp_pdu.c', '                if (on_attr) {\n                    memset(value, 0, sizeof(value));',
     '                if (!on_attr) {\n                    memset(value, 0, sizeof(value));',
     'delivered_value_is_zero_past_its_decoded_bytes'),
]

def run(plant):
    name, path, old, new, test = plant
    work = ROOT / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(SRC, work / 'src', ignore=shutil.ignore_patterns('.git'))
    f = work / 'src' / path
    text = f.read_text()
    if text.count(old) != 1:
        return name, 'FIXTURE', f'{text.count(old)} occurrences'
    f.write_text(text.replace(old, new))
    b = work / 'build'
    cfg = subprocess.run(['cmake', '-S', str(work / 'src'), '-B', str(b), '-DCMAKE_BUILD_TYPE=Debug', '-DLWSRP_MILAN=OFF'],
                         env=ENV, capture_output=True, text=True)
    bld = subprocess.run(['cmake', '--build', str(b), '--parallel', '2'], env=ENV, capture_output=True, text=True)
    if cfg.returncode or bld.returncode:
        return name, 'BUILD', bld.stderr[-300:]
    r = subprocess.run([str(b / 'unit_tests')], env=ENV, capture_output=True, text=True, timeout=900)
    failed = sorted({l.split('-> ')[1].strip() for l in r.stdout.splitlines() if 'Failure:' in l and '-> ' in l})
    if test is None:
        return name, 'caught' if failed else 'ESCAPED', ', '.join(failed[:3]) or f'rc {r.returncode}, no failure'
    return name, 'caught' if test in failed else 'ESCAPED', ', '.join(failed[:3]) or f'rc {r.returncode}'

with concurrent.futures.ThreadPoolExecutor(4) as pool:
    results = list(pool.map(run, PLANTS))
for name, verdict, detail in results:
    print(f'[{verdict}] {name}: {detail}')
print(f'lwSRP donor plants: {sum(v == "caught" for _, v, _ in results)} of {len(results)} caught')
