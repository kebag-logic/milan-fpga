#!/usr/bin/env python3
"""Disposable mutation probes for review round R968-1 (PR #1026, head 12ab4b18).

Each probe plants one textual defect in a tracked file of the clone, runs the in-tree checks named for it, records
each check's exit status and last output line, and restores the file's exact bytes. A probe is CAUGHT when at least
one check exits nonzero, ESCAPED otherwise. After the last probe the clone must be clean (git status --porcelain).

usage: python3 -I probe.py CLONE OUT_LOG [PROBE_NAME ...]
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

D = 'tb/verilator/ctrl_service_budget'
PY = [sys.executable, '-I', '-B']
SELF = {name: PY + [f'{D}/{name}.py', '--selftest'] for name in
        ('egress_mii', 'egress_ledger', 'record_classes', 'shape_costs', 'load_grade', 'rows_tiers', 'arty_grade')}
GRADE = PY + [f'{D}/arty_grade.py', '--point', 'arty-4x4']
GRADE1 = PY + [f'{D}/arty_grade.py', '--point', 'arty-1x1']
#: The service self-test's own check lists, run without its mutant pass (the mutants are the suite's, not the probe's).
BIND = PY + ['-c', "import sys; sys.path.insert(0, 'tb/verilator/ctrl_service_budget'); import selftest, selftest_bind;"
             "bad = [n for n, ok, _ in selftest_bind.bind_checks(selftest) if not ok]; print(bad or 'bind checks hold');"
             "raise SystemExit(bool(bad))"]
SHARE = PY + ['-c', "import sys; sys.path.insert(0, 'tb/verilator/ctrl_service_budget'); import selftest, selftest_share;"
              "import inspect; src = inspect.getsource(selftest_share.clock_checks); print('clock_checks present');"
              "raise SystemExit(0)"]

#: name: (file, old, new, what it plants, checks)
PROBES = {
    'M1-no-crf': (f'{D}/egress_mii.py',
                  "    crf = (SR_HEADER + CRF_AVTPDU,) if (cfg['clocking'].get('crf_output') or {}).get('enabled') "
                  "else ()\n", "    crf = ()\n",
                  "the CRF output's frame is not counted in the 100 Mb/s queue's stream load",
                  ('egress_mii', 'egress_ledger', 'record_classes', 'shape_costs', 'load_grade', 'arty_grade', GRADE)),
    'M2-clock-80': ('configs/endstation_arty_split_4x4.yaml', 'sys_clk_hz: 100000000 ', 'sys_clk_hz: 80000000 ',
                    'the 4x4 configuration runs sys at 80 MHz', (GRADE, 'arty_grade', 'record_classes')),
    'M3-pace-10': ('sw/firmware/ctrl/loop/ctrl_loop.h', '#define AECP_NOTICE_US 195u\n#define AECP_PACE_MS 5u',
                   '#define AECP_NOTICE_US 195u\n#define AECP_PACE_MS 10u',
                   "the (1,5,5) row paces AECP at the 1x1's 10 ms", (GRADE, 'shape_costs', 'rows_tiers')),
    'M4-slice-1000': ('sw/firmware/ctrl/loop/ctrl_loop.h',
                      '#define CTRL_LOOP_SLICE_US 1250u\n#define CTRL_LOOP_BUILD_PASS_US 825u',
                      '#define CTRL_LOOP_SLICE_US 1000u\n#define CTRL_LOOP_BUILD_PASS_US 825u',
                      'the (1,5,5) row takes a 1000 us slice', (GRADE, 'shape_costs')),
    'M5-tx-28': ('sw/firmware/ctrl/loop/ctrl_loop.h', '#define CTRL_LOOP_TX_MS 29u\n#define CTRL_LOOP_STEP_PASS_US 850u',
                 '#define CTRL_LOOP_TX_MS 28u\n#define CTRL_LOOP_STEP_PASS_US 850u',
                 "the (1,5,5) row states the instant-egress census's 28 ms transmit bound", (GRADE, 'shape_costs')),
    'M6-timer-75': (f'{D}/load_grade.py',
                    "        'event.ADP': 75, 'event.ACMP': 165, 'event.MAAP': 160, 'event.AECP': 180, 'event.TICK': 35,"
                    " 'event.GM': 35,\n        'centisecond': 190, 'events_none': 35, 'item.retained': 300, "
                    "'item.aecp.notice': 160,\n        'item.aecp.response': 45, 'item.aecp.probe': 45},\n    '1x1/1if': "
                    "{'record.srp': 285, 'record.aecp': 255, 'record.acmp': 280,",
                    "        'event.ADP': 75, 'event.ACMP': 165, 'event.MAAP': 160, 'event.AECP': 75, 'event.TICK': 35,"
                    " 'event.GM': 35,\n        'centisecond': 190, 'events_none': 35, 'item.retained': 300, "
                    "'item.aecp.notice': 160,\n        'item.aecp.response': 45, 'item.aecp.probe': 45},\n    '1x1/1if': "
                    "{'record.srp': 285, 'record.aecp': 255, 'record.acmp': 280,",
                    "arty-4x4's AECP timer event is stated at the instant-egress 75 us, not the link-rate 180 us",
                    (GRADE, 'load_grade', 'rows_tiers', 'shape_costs')),
    'M7-flight-500': (f'{D}/bind_save.py', "'arty-1x1': 400, 'arty-4x4': 550}", "'arty-1x1': 400, 'arty-4x4': 500}",
                      'the 4x4 in-flight bind bound is 500 ms', (BIND,)),
    'M8-point-name': (f'{D}/record_classes.py', "'endstation_arty_split_4x4': 'arty-4x4'}",
                      "'endstation_arty_split_4x4': 'arty-1x1'}",
                      "a 4x4 build's records are graded at the 1x1's stated costs", ('record_classes', GRADE)),
    'M9-record-acmp': (f'{D}/poll_grade.py',
                       "    arty = {shape_costs.Shape(1, 1, 2): 'arty-1x1', shape_costs.Shape(1, 5, 5): 'arty-4x4'}",
                       "    arty = {shape_costs.Shape(1, 1, 2): 'arty-1x1', shape_costs.Shape(1, 5, 5): 'arty-1x1'}",
                       "the (1,5,5) ACMP record is the 1x1's", (GRADE, 'record_classes', 'rows_tiers', 'load_grade')),
    'M10-arty-clock': (f'{D}/record_classes.py', "ARTY_CLOCKS = {'arty-1x1': 80_000_000, 'arty-4x4': 100_000_000}",
                       "ARTY_CLOCKS = {'arty-1x1': 80_000_000, 'arty-4x4': 80_000_000}",
                       'a 4x4 leg is held to 80 MHz', ('record_classes', GRADE)),
    'M11-doc-acmp': ('docs/design/SPLIT_CONTROL_MEMORY.md', '| ACMP | 28.52 ms | 30 ms |', '| ACMP | 27.52 ms | 30 ms |',
                     "section 15's 4x4 ACMP row is not the model's",
                     (GRADE, 'arty_grade', 'rows_tiers', 'load_grade', 'shape_costs', 'egress_ledger')),
    'M12-doc-ledger': ('docs/design/SPLIT_CONTROL_MEMORY.md', '| `backlog.owed_behind3.if0` | 63.32736 | 63.50 |',
                       '| `backlog.owed_behind3.if0` | 63.32736 | 63.60 |',
                       "section 15's 4x4 ledger figure is a tenth over the rule", ('egress_ledger',)),
    'M13-ledger-measured': (f'{D}/egress_ledger.py', "'backlog.owed_behind3.if0': 63.32736, 'backlog-owed.service.acmp."
                            "last.if0': 61.81513,", "'backlog.owed_behind3.if0': 63.42736, 'backlog-owed.service.acmp."
                            "last.if0': 61.81513,", "ARTY_4X4's largest measurement is raised 0.1 ms",
                            ('egress_ledger',)),
    'M14-static-assert': ('sw/firmware/ctrl/loop/ctrl_loop.c',
                          'CTRL_LOOP_SHAPE(1u, 1u, 2u) || CTRL_LOOP_SHAPE(1u, 5u, 5u)) ||',
                          'CTRL_LOOP_SHAPE(1u, 1u, 2u)) ||',
                          'the transmit-bound assertion does not cover the (1,5,5) shape',
                          (GRADE, 'shape_costs', 'rows_tiers')),
    'M15-edit-paced': (f'{D}/edit_rows.py', "'arty-4x4': {'a one-row edit': 255, 'an accepted SET_CONFIGURATION': 410},",
                       "'arty-4x4': {'a one-row edit': 155, 'an accepted SET_CONFIGURATION': 210},",
                       "arty-4x4's paced edit costs are understated", (GRADE, 'record_classes', 'rows_tiers', 'load_grade')),
    'M16-long-record': (f'{D}/rows_tiers.py', "'arty-1x1': 1105, 'arty-4x4': 890,", "'arty-1x1': 1105, 'arty-4x4': 490,",
                        "arty-4x4's largest AECP record is understated", (GRADE, 'rows_tiers', 'record_classes')),
}


def run(cmd: list[str], clone: Path) -> tuple[int, str]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    done = subprocess.run(cmd, cwd=clone, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                          timeout=900)
    lines = [line for line in done.stdout.splitlines() if line.strip()]
    refused = [line for line in lines if line.startswith(('REFUSED', 'FAIL', 'ESCAPED', 'MISSED'))]
    return done.returncode, (refused[0] if refused else (lines[-1] if lines else ''))[:260]


def main(argv: list[str]) -> int:
    clone, out = Path(argv[0]).resolve(), Path(argv[1])
    names = argv[2:] or list(PROBES)
    report = []
    for name in names:
        path, old, new, what, checks = PROBES[name]
        target = clone / path
        original = target.read_bytes()
        text = original.decode()
        if text.count(old) != 1:
            report.append(f'{name}: NOT PLANTED ({text.count(old)} matches in {path})')
            continue
        try:
            target.write_bytes(text.replace(old, new).encode())
            rows = []
            for check in checks:
                cmd = SELF[check] if isinstance(check, str) else check
                label = (f'{check} --selftest' if isinstance(check, str) else
                         ' '.join(cmd[3:])[:60] if cmd[3] != '-c' else 'service self-test check list')
                rc, last = run(cmd, clone)
                rows.append((label, rc, last))
        finally:
            target.write_bytes(original)
        caught = any(rc for _, rc, _ in rows)
        report.append(f'{name}: {"CAUGHT" if caught else "ESCAPED"} - {what} ({path})')
        report += [f'    rc={rc} {label}: {last}' for label, rc, last in rows]
    status = subprocess.run(['git', 'status', '--porcelain'], cwd=clone, stdout=subprocess.PIPE, text=True).stdout
    report.append('clone after probes: ' + ('clean' if not status.strip() else 'DIRTY\n' + status))
    out.write_text('\n'.join(report) + '\n')
    print('\n'.join(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
