# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The host model's access counts the scenario publishes for ADP's paths, held to the adapter's own bounds.

Each ADP probe carries `accesses`, the mailbox accesses the host model measures or bounds for its pass
(scenario.Probe). grade.py copies it to a row's `model_accesses` and run.py prints it beside the measured row. The
adapter states the same counts as ADP_MBX_LAT_* (sw/firmware/ctrl/adp/adp_mbx.h), and test_adp.cpp's C0 to C6
measure them on the host model.

The budget image is the size fixture's composition, which wires no clock (adp_mbx_set_clock), so the seed's sample
is the NOW_MS fallback: LINK_UP's pass is 12 accesses (ADP_MBX_LAT_LINK). The platform wires the microsecond clock,
and its LINK_UP pass is 11; that path is the platform's, not this harness's.

A probe whose count differs from the header's is a finding: a stale count in the evidence. The self-test runs the
real scenario (no finding) and the same scenario with LINK_UP's count planted back at 11 (one finding a point).
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scenario  # noqa: E402

HEADER = HERE.parents[2] / 'sw/firmware/ctrl/adp/adp_mbx.h'
ORACLE = HERE / 'oracle.json'
#: Each ADP path the scenario probes, and the ADP_MBX_LAT_* bound its count is.
PATHS = {'adp.link_up': 'LINK', 'adp.gm_change': 'GM', 'adp.discover': 'DISCOVER', 'adp.tmr_delay': 'DELAY',
         'adp.tmr_advertise': 'ADVERTISE'}


def bounds(text: str) -> dict[str, int]:
    """ADP_MBX_LAT_<path> -> its count, from the adapter header's text."""
    return {name: int(count) for name, count in re.findall(r'#define ADP_MBX_LAT_(\w+) (\d+)u', text)}


def path_of(probe: scenario.Probe) -> str:
    """The path a probe is an instance of: its own, else its name without `.if<n>`."""
    return probe.path or re.sub(r'\.if\d+$', '', probe.name)


def findings(groups: list[scenario.Group], counts: dict[str, int]) -> list[str]:
    """Each ADP probe whose published count differs from the adapter's bound for its path."""
    out = []
    for g in groups:
        for probe in g.probes:
            name = PATHS.get(path_of(probe))
            if name is not None and probe.accesses != counts[name]:
                out.append(f'{g.name}: {probe.name} publishes {probe.accesses} model accesses, '
                           f'ADP_MBX_LAT_{name} is {counts[name]}')
    return out


def groups_at(p: scenario.Point) -> list[scenario.Group]:
    """The scenario's groups that carry ADP's counts: the advertised links, the ADP groups, the fixture's."""
    return [*scenario.adp_groups(p), *scenario.control_groups(p), *scenario.fixture_groups(p)]


def stale(groups: list[scenario.Group]) -> list[scenario.Group]:
    """The same groups with LINK_UP's count planted back at 11, the count before the fallback's sample."""
    for g in groups:
        g.probes = [replace(pr, accesses=11) if path_of(pr) == 'adp.link_up' else pr for pr in g.probes]
    return groups


def main() -> int:
    """The check at one and two interfaces, and its planted stale count; 0 when both behave."""
    counts = bounds(HEADER.read_text(encoding='utf-8'))
    base = json.loads(ORACLE.read_text(encoding='utf-8'))['point']
    failures = 0
    for interfaces in (1, 2):
        p = scenario.Point(**dict(base, interfaces=interfaces))
        found = findings(groups_at(p), counts)
        planted = findings(stale(groups_at(p)), counts)
        ok = not found and len(planted) >= interfaces
        failures += not ok
        print(f'MODEL COUNTS {interfaces} interface(s): {len(found)} stale count(s) in the scenario; '
              f'the planted 11 found {len(planted)} time(s): {"ok" if ok else "FAIL"}')
        for line in found:
            print(f'  {line}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
