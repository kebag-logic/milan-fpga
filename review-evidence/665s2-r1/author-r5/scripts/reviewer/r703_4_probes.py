#!/usr/bin/env python3
"""Round-4 reviewer probes on tb/verilator/ctrl_service_budget at the reviewed head.

Usage: python3 -I r703_4_probes.py <checkout> <out-dir>

Each mutant edits one file of the checkout's harness by an exact, unique string
replacement, runs `run.py --self-test`, records whether the self-test failed
(caught) or passed (escaped), and restores the file's exact bytes. A final
`git status --porcelain` must be empty. A demonstration (D1) calls
run.composed_maximum on synthetic window sets without any edit.
"""
import json
import subprocess
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
H = CHECKOUT / 'tb/verilator/ctrl_service_budget'

MUTANTS = {
    'P1 BACKLOG_ROWS drops backlog-adp-refill (the 8x8 arm A composed maximum row)': (
        'grade.py', "BACKLOG_ROWS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')",
        "BACKLOG_ROWS = ('backlog', 'backlog-adp', 'backlog-owed')"),
    'P2 BACKLOG_ROWS drops backlog-owed': (
        'grade.py', "BACKLOG_ROWS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')",
        "BACKLOG_ROWS = ('backlog', 'backlog-adp', 'backlog-adp-refill')"),
    'P3 table drops the "at least" prefix of a lower-bound composed maximum': (
        'run.py', "f\"{'at least ' if top['lower_bound'] else ''}{top['cycles']:,} CPU cycles",
        "f\"{top['cycles']:,} CPU cycles"),
    'P4 table drops the lower-bound clause': (
        'run.py', "bound = f\", a lower bound (load unreleased in {', '.join(top['unreleased'])})\" if top['lower_bound'] else ''",
        "bound = ''"),
    'P5 results.json omits composed_maximum': (
        'run.py', 'composed_maximum=composed_maximum(results),', 'composed_maximum=None,'),
    'P6 fan-out recipients not sorted by commit before first/last': (
        'grade.py', 'cycles = sorted(c for c in grader.recipients(spec, probe, start, next_mark)[0].values() if c is not None)',
        'cycles = [c for c in grader.recipients(spec, probe, start, next_mark)[0].values() if c is not None]'),
    'P7 composed maximum labelled lower bound only when its own window is unreleased': (
        'run.py', "lower_bound=not all(w['serviced'] for w in every),", "lower_bound=not top['serviced'],"),
    'P8 released figure taken over every window': (
        'run.py', "done = max((w for w in every if w['serviced']), key=lambda w: w['cycles'], default=None)",
        "done = max(every, key=lambda w: w['cycles'], default=None)"),
    'P9 service ahead counts a record released exactly at the commit': (
        'grade.py', 'ahead=sum(1 for _, _, r in records[:n] if r is None or r > commit),',
        'ahead=sum(1 for _, _, r in records[:n] if r is None or r >= commit),'),
    'P10 service ahead counts every earlier record': (
        'grade.py', 'ahead=sum(1 for _, _, r in records[:n] if r is None or r > commit),',
        'ahead=n,'),
}


def selftest() -> tuple[int, str]:
    p = subprocess.run([sys.executable, '-B', str(H / 'run.py'), '--self-test'], cwd=CHECKOUT,
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout + p.stderr


def demo() -> dict:
    sys.path.insert(0, str(H))
    import run  # noqa: E402
    win = lambda g, cyc, done: dict(group=g, probes=[], timeouts=[], passes=dict(composed=dict(
        cycles=cyc, ms=cyc / 50_000, passes=3, window_ms=100.0, serviced=done, unreleased={} if done else {'srp': 32})))
    # Arm B as published runs three of the four backlog rows (README.md:59, no backlog-adp-refill).
    arm_b_1x1 = [win('backlog', 740_260, True), win('backlog-adp', 645_058, True), win('backlog-owed', 582_392, True)]
    one_row = [win('backlog', 740_260, True)]
    return {'arm_b_1x1_three_rows': run.composed_maximum(arm_b_1x1),
            'one_row_only': run.composed_maximum(one_row),
            'table_one_row': [l for l in run.table([dict(w, point='1x1') for w in one_row], '1x1').splitlines()
                              if l.startswith('Composed maximum')] if hasattr(run, 'table') else None}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {}
    rc0, _ = selftest()
    report['baseline_selftest_rc'] = rc0
    for name, (rel, old, new) in MUTANTS.items():
        path = H / rel
        orig = path.read_bytes()
        text = orig.decode()
        if text.count(old) != 1:
            report[name] = 'ANCHOR NOT UNIQUE'
            continue
        try:
            path.write_text(text.replace(old, new))
            rc, log = selftest()
        finally:
            path.write_bytes(orig)
        fails = [l for l in log.splitlines() if l.startswith('FAIL')][:3]
        report[name] = dict(verdict='caught' if rc != 0 else 'ESCAPED', rc=rc, first_failures=fails)
    try:
        report['D1 demonstration'] = demo()
    except Exception as e:  # recorded, not hidden
        report['D1 demonstration'] = f'error: {e!r}'
    st = subprocess.run(['git', 'status', '--porcelain'], cwd=CHECKOUT, capture_output=True, text=True).stdout
    report['git_status_porcelain_after'] = st
    (OUT / 'probes.json').write_text(json.dumps(report, indent=1, default=str) + '\n')
    print(json.dumps(report, indent=1, default=str))
    return 0 if not st and rc0 == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
