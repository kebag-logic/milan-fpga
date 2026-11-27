# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The host model's access counts the scenario publishes for ADP's paths, held to the adapter's own counts.

A probe may carry `accesses`, the mailbox accesses the host model measures or bounds for its pass (scenario.Probe).
grade.py copies it to a row's `model_accesses` and run.py prints it beside the measured row. The adapter states ADP's
counts in sw/firmware/ctrl/adp/adp_mbx.h, and test_adp.cpp's C0 to C6 bound them on the host model.

The scenario publishes counts for seven ADP paths, and this check holds all seven (PATHS):
- adp.link_up, adp.gm_change, adp.discover, adp.tmr_delay, adp.tmr_advertise and adp.shutdown, each to its
  ADP_MBX_LAT_* macro;
- adp.link_down, to the count the header states in ADP_MBX_LAT_LINK's comment, "(down, a stop: 9)". It has no macro
  of its own: C5 bounds it by ADP_MBX_LAT_LINK.
A header that no longer states one of the seven counts makes the check raise, not pass.

The budget image is the size fixture's composition, which wires no clock (adp_mbx_set_clock), so the seed's sample
is the NOW_MS fallback: LINK_UP's pass is 12 accesses (ADP_MBX_LAT_LINK). The platform wires the microsecond clock,
and its LINK_UP pass is 11; that path is the platform's, not this harness's.

The check reads every build-free group set (SETS). The build-dependent sets (AECP, the reboot, the save window, the
long notice) publish no count. An ADP probe that publishes a count on a path outside the seven is a finding too.

A probe whose count differs from the header's is a finding: a stale count in the evidence. The self-test runs the
real scenario, which must give no finding. It then plants each path's count one short, and every instance of that
path must be found.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import datapath_window, held, kept_window, scenario  # noqa: E402,E401

HEADER = HERE.parents[2] / 'sw/firmware/ctrl/adp/adp_mbx.h'
ORACLE = HERE / 'oracle.json'
#: Each ADP path the scenario publishes a count for, and the header's count it is held to.
PATHS = {'adp.link_up': 'LINK', 'adp.link_down': 'LINK_DOWN', 'adp.gm_change': 'GM', 'adp.discover': 'DISCOVER',
         'adp.tmr_delay': 'DELAY', 'adp.tmr_advertise': 'ADVERTISE', 'adp.shutdown': 'SHUTDOWN'}
#: The build-free group sets of scenario.all_groups; the others publish no count.
SETS = (scenario.acmp_groups, scenario.adp_groups, scenario.backlog_groups, scenario.bound_talker_groups,
        scenario.control_groups, scenario.fixture_groups, scenario.maap_groups, scenario.shutdown_groups,
        scenario.srp_groups, kept_window.groups, datapath_window.groups, held.groups)


def bounds(text: str) -> dict[str, int]:
    """ADP_MBX_LAT_<path> -> its count, and LINK_DOWN's from the LINK macro's comment, from the header's text."""
    counts = {name: int(count) for name, count in re.findall(r'#define ADP_MBX_LAT_(\w+) (\d+)u', text)}
    down = re.search(r'#define ADP_MBX_LAT_LINK \d+u\s*//.*\(down, a stop: (\d+)\)', text)
    return counts | ({'LINK_DOWN': int(down.group(1))} if down else {})


def path_of(probe: scenario.Probe) -> str:
    """The path a probe is an instance of: its own, else its name without `.if<n>`."""
    return probe.path or re.sub(r'\.if\d+$', '', probe.name)


def counted(groups: list[scenario.Group]) -> list[tuple[str, scenario.Probe]]:
    """(group, probe) for each ADP probe that publishes a count."""
    return [(g.name, pr) for g in groups for pr in g.probes if pr.family == 'adp' and pr.accesses is not None]


def findings(groups: list[scenario.Group], counts: dict[str, int]) -> list[str]:
    """Each ADP probe whose published count differs from the header's for its path, or whose path is not held."""
    out = []
    for group, probe in counted(groups):
        name = PATHS.get(path_of(probe))
        if name is None:
            out.append(f'{group}: {probe.name} publishes {probe.accesses} model accesses on a path not held here')
        elif probe.accesses != counts[name]:
            out.append(f'{group}: {probe.name} publishes {probe.accesses} model accesses, the header states '
                       f'{counts[name]} ({name})')
    return out


def groups_at(p: scenario.Point) -> list[scenario.Group]:
    """Every build-free group of a point, built afresh."""
    return [g for make in SETS for g in make(p)]


def stale(groups: list[scenario.Group], path: str, count: int) -> list[scenario.Group]:
    """The same groups with every instance of `path` publishing `count`."""
    for g in groups:
        g.probes = [replace(pr, accesses=count) if path_of(pr) == path else pr for pr in g.probes]
    return groups


def main() -> int:
    """The check at one and two interfaces, and each path's planted stale count; 0 when all behave."""
    counts = bounds(HEADER.read_text(encoding='utf-8'))
    base = json.loads(ORACLE.read_text(encoding='utf-8'))['point']
    failures = 0
    for interfaces in (1, 2):
        p = scenario.Point(**dict(base, interfaces=interfaces))
        found = findings(groups_at(p), counts)
        instances = {path: sum(path_of(pr) == path for _, pr in counted(groups_at(p))) for path in PATHS}
        caught = {path: len(findings(stale(groups_at(p), path, counts[name] - 1), counts))
                  for path, name in PATHS.items()}
        ok = not found and all(instances[path] and caught[path] == instances[path] for path in PATHS)
        failures += not ok
        plants = ', '.join(f'{path[4:]} {counts[name] - 1} {caught[path]}/{instances[path]}'
                           for path, name in PATHS.items())
        print(f'MODEL COUNTS {interfaces} interface(s): {len(found)} stale count(s) in the scenario; '
              f'each path planted one short, found/instances: {plants}: {"ok" if ok else "FAIL"}')
        for line in found:
            print(f'  {line}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
