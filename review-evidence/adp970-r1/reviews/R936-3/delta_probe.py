#!/usr/bin/env python3
"""Exercise count consistency and prove unchanged stimuli and grading on recorded input."""
import copy
import dataclasses
import json
import subprocess
import sys
import types
from pathlib import Path
from unittest.mock import patch

repo, packet = map(Path, sys.argv[1:3])
budget = repo / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(budget))
import model_counts as mc
import scenario
import grade
import run

before = types.ModuleType('scenario_before')
before.__file__ = str(budget / 'scenario.py')
sys.modules[before.__name__] = before
source = subprocess.check_output(['git', '-C', str(repo), 'show', 'f4833e16:tb/verilator/ctrl_service_budget/scenario.py'])
exec(compile(source, before.__file__, 'exec'), before.__dict__)
oracle = json.loads((budget / 'oracle.json').read_text())
counts = mc.bounds(mc.HEADER.read_text())
constructors = ['adp_groups', 'control_groups', 'fixture_groups']
out = []
for label, (shape, interfaces) in run.POINTS.items():
    fields = dict(oracle['point'], label=label, shape=shape, interfaces=interfaces)
    oldp, newp = before.Point(**fields), scenario.Point(**fields)
    changes = []
    current = []
    for name in constructors:
        old = getattr(before, name)(oldp)
        new = getattr(scenario, name)(newp)
        current.extend(new)
        assert len(old) == len(new)
        for a, b in zip(old, new):
            assert a.script() == b.script(), (label, name, a.name, 'stimulus')
            ad, bd = dataclasses.asdict(a), dataclasses.asdict(b)
            for ap, bp in zip(ad['probes'], bd['probes']):
                if ap['accesses'] != bp['accesses']:
                    assert mc.path_of(scenario.Probe(**bp)) == 'adp.link_up'
                    assert (ap['accesses'], bp['accesses']) == (11, 12)
                    changes.append((b.name, bp['name'], 11, 12))
                ap.pop('accesses'); bp.pop('accesses')
            assert ad == bd, (label, name, a.name, 'other fields')
    assert not mc.findings(current, counts)
    stale = mc.findings(mc.stale(copy.deepcopy(current)), counts)
    assert len(stale) == len(changes) == 5 * interfaces + 1
    # Falsify each construction site independently, including explicit path and suffix resolution.
    for constructor in ('advertised', 'fixture'):
        groups = copy.deepcopy(current)
        planted = 0
        for g in groups:
            for pr in g.probes:
                if mc.path_of(pr) == 'adp.link_up' and ((g.name == 'fixture') == (constructor == 'fixture')):
                    pr.accesses = 11
                    planted += 1
        assert len(mc.findings(groups, counts)) == planted > 0
    # Every checked non-LINK path must reject an independent stale count too.
    for path in mc.PATHS:
        groups = copy.deepcopy(current)
        pr = next(pr for g in groups for pr in g.probes if mc.path_of(pr) == path)
        pr.accesses += 1
        assert len(mc.findings(groups, counts)) == 1, path
    print(f'PASS {label}: {len(changes)} LINK_UP fields 11 -> 12; all stimuli, waits, budgets and other fields identical; both sites and all five checked paths detect stale values')
    out.append(dict(point=label, changes=changes, stale_found=len(stale)))

# A real committed trace, graded with each scenario version: only the model metadata may differ.
point = scenario.Point(**oracle['point'])
oldpoint = before.Point(**oracle['point'])
trace = (budget / 'fixture.log').read_text()
old = grade.grade(trace, before.fixture_groups(oldpoint)[0], 100_000_000, 50_000_000)
new = grade.grade(trace, scenario.fixture_groups(point)[0], 100_000_000, 50_000_000)
old_row = next(p for p in old['probes'] if p['probe'] == 'fixture.link_up.if0')
new_row = next(p for p in new['probes'] if p['probe'] == 'fixture.link_up.if0')
assert old_row['model_accesses'] == 11 and new_row['model_accesses'] == 12
old_row['model_accesses'] = 12
assert old == new, 'timing, verdict or another graded value changed'
table = run.table([new], '1x1')
line = next(line for line in table.splitlines() if '`fixture.link_up.if0` |' in line)
assert ' (12) |' in line
print('PASS recorded fixture: every timing, verdict, measured access count and composed result unchanged')
print('Generated corrected table row:', line)
(packet / 'fixture-regraded.json').write_text(json.dumps(new, indent=2) + '\n')
(packet / 'fixture-table.md').write_text(table + '\n')
(packet / 'delta-probe.json').write_text(json.dumps(out, indent=2) + '\n')
assert mc.main() == 0

# Exercise run.py's actual dispatch without repeating its expensive fixture campaign.
import selftest
old_groups = lambda p: [*before.adp_groups(p), *before.control_groups(p), *before.fixture_groups(p)]
with patch.object(sys, 'argv', ['run.py', '--self-test']):
    with patch.object(mc, 'groups_at', old_groups), patch.object(selftest, 'main') as downstream:
        assert run.main() == 1
        downstream.assert_not_called()
    with patch.object(selftest, 'main', return_value=7) as downstream:
        assert run.main() == 7
        downstream.assert_called_once_with([])
print('PASS dispatch: stale metadata fails before fixture; clean metadata reaches fixture and propagates its failure')
