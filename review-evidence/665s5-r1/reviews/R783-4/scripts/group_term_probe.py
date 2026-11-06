#!/usr/bin/env python3
"""Whether the supersede rule's group term decides anything on the groups this harness really runs: which groups, at
each point, carry a probe of a tabled path on which interface.

usage: group_term_probe.py <tree extracted at the exact head>
"""
import collections
import dataclasses
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(TREE / 'tb/verilator/ctrl_service_hooks'))
import hooks_selftest as t  # noqa: E402
hooks, hooks_build = t.hooks, t.hooks_build

for name, point in (('1 interface', t.POINT), ('2 interfaces', dataclasses.replace(t.POINT, interfaces=2))):
    scenario = t.scenario
    made = [*scenario.acmp_groups(point), *scenario.adp_groups(point), *scenario.control_groups(point),
            hooks.loaded_notify_group(point), hooks.order_adp_group(point), hooks.order_acmp_group(point),
            hooks.aging_group(point), *hooks.late_groups(point)]
    where = collections.defaultdict(list)
    for g in made:
        for p in g.probes:
            key = p.path_key
            key = key() if callable(key) else key
            if key[0] in hooks.SUPERSEDED:
                where[key].append(g.name)
    print(name, 'groups', len(made), {k: v for k, v in sorted(where.items())})
    print('  (path, interface) carried by more than one group:', {k: v for k, v in where.items() if len(set(v)) > 1})
