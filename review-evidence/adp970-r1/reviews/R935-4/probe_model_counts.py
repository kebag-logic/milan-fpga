"""Disposable in-memory probes of tb/verilator/ctrl_service_budget/model_counts.py (no file is edited).

Usage: python3 -I probe_model_counts.py <repository root>

Each probe changes the header text, the scenario's published counts or the check's own tables in memory and
reports whether the check finds (DETECTED), raises (RAISES) or passes (MISSED). Exit 0 when every probe behaves as
expected.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
HERE = ROOT / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(HERE))
import model_counts as mc  # noqa: E402
import scenario  # noqa: E402

TEXT = mc.HEADER.read_text(encoding='utf-8')
BASE = json.loads(mc.ORACLE.read_text(encoding='utf-8'))['point']


def header_with(name: str, value: int) -> str:
    return re.sub(rf'(#define ADP_MBX_LAT_{name} )\d+u', rf'\g<1>{value}u', TEXT)


def outcome(fn) -> str:
    try:
        return 'DETECTED' if fn() else 'MISSED'
    except Exception as e:  # noqa: BLE001
        return f'RAISES ({type(e).__name__})'


def at(interfaces: int):
    return scenario.Point(**dict(BASE, interfaces=interfaces))


def main() -> int:
    bad = 0
    rows = []
    for n in (1, 2):
        p = at(n)
        real = mc.bounds(TEXT)
        rows.append((n, 'real header, real scenario', outcome(lambda: mc.findings(mc.groups_at(p), real)), 'MISSED'))
        for name in ('LINK', 'GM', 'DISCOVER', 'DELAY', 'ADVERTISE', 'SHUTDOWN'):
            h = mc.bounds(header_with(name, real[name] + 1))
            rows.append((n, f'header {name} {real[name] + 1}', outcome(lambda: mc.findings(mc.groups_at(p), h)),
                         'DETECTED'))
        down = mc.bounds(TEXT.replace('(down, a stop: 9)', '(down, a stop: 10)'))
        rows.append((n, 'header LINK_DOWN comment 10', outcome(lambda: mc.findings(mc.groups_at(p), down)),
                     'DETECTED'))
        gone = mc.bounds(TEXT.replace('(down, a stop: 9)', '(down: 9)'))
        rows.append((n, 'header LINK_DOWN comment unreadable', outcome(lambda: mc.findings(mc.groups_at(p), gone)),
                     'RAISES (KeyError)'))
        nosd = mc.bounds(re.sub(r'#define ADP_MBX_LAT_SHUTDOWN \d+u', '', TEXT))
        rows.append((n, 'header SHUTDOWN macro removed', outcome(lambda: mc.findings(mc.groups_at(p), nosd)),
                     'RAISES (KeyError)'))
        for path, name in mc.PATHS.items():
            plus = real[name] + 1
            rows.append((n, f'scenario {path} {plus} (one over)',
                         outcome(lambda: mc.findings(mc.stale(mc.groups_at(p), path, plus), real)), 'DETECTED'))

        def foreign():
            gs = mc.groups_at(p)
            pr = gs[0].probes[0]
            gs[0].probes.append(replace(pr, name='adp.unheld.if0', family='adp', accesses=5, path=None))
            return mc.findings(gs, real)
        rows.append((n, 'an ADP count on an unheld path', outcome(foreign), 'DETECTED'))

        def one_instance(path: str):
            gs = mc.groups_at(p)
            for g in gs:
                hit = [i for i, pr in enumerate(g.probes) if mc.path_of(pr) == path]
                if hit:
                    g.probes[hit[-1]] = replace(g.probes[hit[-1]], accesses=g.probes[hit[-1]].accesses + 7)
                    break
            return mc.findings(gs, real)
        for path in mc.PATHS:
            rows.append((n, f'one instance of {path} stale', outcome(lambda: one_instance(path)), 'DETECTED'))
    # The check's own main() against weakened tables: each must fail (return nonzero) or raise.
    saved_paths, saved_sets = dict(mc.PATHS), mc.SETS
    for label, paths, sets in (
            ('PATHS without adp.shutdown', {k: v for k, v in saved_paths.items() if k != 'adp.shutdown'}, saved_sets),
            ('PATHS without adp.link_down', {k: v for k, v in saved_paths.items() if k != 'adp.link_down'},
             saved_sets),
            ('SETS without shutdown_groups', saved_paths, tuple(s for s in saved_sets if s is not
                                                                 scenario.shutdown_groups)),
            ('SETS without adp_groups', saved_paths, tuple(s for s in saved_sets if s is not scenario.adp_groups))):
        mc.PATHS.clear()
        mc.PATHS.update(paths)
        mc.SETS = sets
        try:
            rc = mc.main()
            res = 'main FAILS' if rc else 'main PASSES'
        except Exception as e:  # noqa: BLE001
            res = f'main RAISES ({type(e).__name__})'
        rows.append(('-', f'weakened check: {label}', res, 'main FAILS'))
        mc.PATHS.clear()
        mc.PATHS.update(saved_paths)
        mc.SETS = saved_sets
    for n, what, got, want in rows:
        ok = got == want or (want == 'main FAILS' and got.startswith('main RAISES'))
        bad += not ok
        print(f'{"ok  " if ok else "FAIL"} [{n} if] {what}: {got} (expected {want})')
    print(f'PROBES: {len(rows) - bad} of {len(rows)} as expected')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
