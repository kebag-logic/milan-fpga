#!/usr/bin/env python3
"""Round 7's receipts (round 6's rcpt_r6.py, the lane gates' parts given) from the pass's own outputs, host paths replaced by placeholders (round 4's receipts'
forms): the lane gates (each gate's rc and the last line of its log, in the order they ended, and each part's clone
status after it ran), the firmware jobs (each step's rc and the campaigns' tallies) and one unit's log (the counters-f5
make and Q-img). Prints the receipt; exits 1 when a lane gate's rc is not 0 and its name does not end _exits_1, or a
firmware step's rc is not 0.
usage: rcpt_r7.py lane HEAD FULL PARTS | firmware HEAD FULL | unit NAME TITLE | sweep HEAD OUT LABEL SHARD"""
import re
import subprocess
import sys
from pathlib import Path

T = '/data-2/milan/tmp/894b-a781'
SUBS = ((T, '<scratch>'), ('$WORKSPACE_HOME', '<home>'), ('$VALIDATION_STORAGE', '<data>'), ('/data-2/milan', '<data-2>'))


def clean(text: str) -> str:
    for a, b in SUBS:
        text = text.replace(a, b)
    return text


def last(path: Path) -> str:
    lines = [l for l in path.read_text(errors='replace').splitlines() if l.strip()]
    return lines[-1] if lines else '(empty)'


def lane(head: str, full: Path, parts: str = 'abc') -> int:
    g = full / 'lane'
    order = [l.split()[1] for l in (g / 'summary.txt').read_text().splitlines()
             if len(l.split()) == 3 and l.split()[2].startswith('rc=')]
    print(f'# the lane gates at {head[:8]} (lane_gates_r7.sh, part(s) {", ".join(parts)}, each on its own clean clone of the head, '
          f'never piped): each gate\'s rc and its last line; {len(order)} gates; those that exit 1 by design are named so '
          '(_exits_1)')
    bad = 0
    for gate in order:
        rc = (g / f'{gate}.rc').read_text().strip()
        ok = rc == '0' or (gate.endswith('_exits_1') and rc == '1')
        bad += not ok
        print(clean(f'{gate} rc={rc}: {last(g / f"{gate}.log")}') + ('' if ok else '   <-- FAIL'))
    print('\n# each part\'s clone after it ran (git status --short --untracked-files=all):')
    for part in parts:
        w = full / f'gate-wt-{part}'
        n = subprocess.run(['git', '-C', str(w), 'status', '--short', '--untracked-files=all'], capture_output=True,
                           text=True, check=True).stdout.splitlines()
        h = subprocess.run(['git', '-C', str(w), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        print(f'part {part}: at {h[:8]}, {len(n)} line(s)')
        bad += bool(n) or h != head
    print(f'\n{len(order)} gates, {bad} bad')
    return int(bad > 0)


TALLY = re.compile(r'test_ctrl_firmware: (PASS|FAIL)|ctrl_boundary: .*|aecp_wire\.py --every: .*|ALL GATES PASS.*|RESULT: .*')


def firmware(head: str, full: Path) -> int:
    logs = full / 'wf' / 'logs'
    print(f'# the firmware jobs at {head[:8]} (run_wf.py, each on its own fresh clean clone of the head): every step\'s rc, '
          'and the campaigns\' tallies')
    bad = 0
    for job in ('firmware-unit', 'firmware-boundary', 'firmware-control-mutants', 'firmware-aecp-mutants',
                'firmware-srp-mutants', 'firmware-verilator'):
        rcs = sorted(logs.glob(f'rtl-fast__{job}__*.rc'))
        if not rcs:
            print(f'{job}: NO STEP RAN   <-- FAIL')
            bad += 1
            continue
        steps = {p.name.split('__')[2][:-3]: p.read_text().strip() for p in rcs}
        bad += sum(v != '0' for v in steps.values())
        print(f'{job}: ' + ', '.join(f'{k}={v}' for k, v in sorted(steps.items())))
        for step in sorted(steps):
            log = logs / f'rtl-fast__{job}__{step}.log'
            text = log.read_text(errors='replace').splitlines()
            ok = sum(l.startswith('[ok]') for l in text)
            escaped = sum('ESCAPED' in l for l in text)
            if ok or escaped:
                print(f'  {step}.log: [ok] {ok}, ESCAPED {escaped}')
                bad += escaped > 0
            seen = []
            for l in text:
                m = TALLY.search(l)
                if m and m.group(0) not in seen:
                    seen.append(m.group(0))
            for s in seen:
                print(clean(f'  {step}.log: {s}'))
        after = logs / f'rtl-fast__{job}__tree-after.txt'
        status = after.read_text().split('status:', 1)[-1].split() if after.exists() else ['(no record)']
        print(f'  the clone after it ran: {" ".join(status) or "clean"}')
    print(f'\n{bad} step(s) not rc 0 or with an escaped mutant')
    return int(bad > 0)


def sweep(head: str, out: Path, label: str, k: int) -> int:
    """One shard of native-shards.py's sweep: its exit and finish (complete.json), whether TSN_GEN_ROOT was set, the
    SKIPPED lines its suite logs hold, run_all_suites.sh's own summary (spec/01.log) and the shard unit's CPUs."""
    import json
    d = out / f'shard-{k}'
    done = json.loads((d / 'spec' / 'complete.json').read_text())
    cmd = json.loads((d / 'spec' / 'results.json').read_text())['results'][0]['command']
    skipped = sum(l.count('SKIPPED') for p in (d / 'logs').glob('*.log') for l in p.read_text(errors='replace').splitlines())
    cpus = subprocess.run(['journalctl', '--user', '-u', f'milan-{label}-shard{k}', '--no-pager', '-o', 'cat'],
                          capture_output=True, text=True).stdout
    m = re.search(r'taskset -c ([0-9,-]+)', cpus)
    print(f'# the sweep, shard {k} of 4 (native-shards.py, label {label}) at {head[:8]} on its own fresh clone, '
          f'run-recorded-gates.py: exit {done["exit_code"]}, finished {done["finished"][:19]}; TSN_GEN_ROOT set: '
          f'{any(c.startswith("TSN_GEN_ROOT=") for c in cmd)}; SKIPPED lines {skipped}; the head {done["head"][:8]}')
    print(clean((d / 'spec' / '01.log').read_text(errors='replace')).rstrip())
    print(f'CPUs {m.group(1) if m else "?"} (a cpu_ranges.py pick range, the unit\'s affinity checked at launch)')
    return int(done['exit_code'] != 0 or done['head'] != head)


def unit(name: str, title: str) -> int:
    u = Path(T) / 'units'
    rc = (u / f'{name}.rc').read_text().strip()
    print(f'# {title}')
    print(clean((u / f'{name}.log').read_text(errors='replace')).rstrip())
    print(f'unit rc={rc}')
    return int(rc != '0')


if __name__ == '__main__':
    kind = sys.argv[1]
    if kind == 'unit':
        sys.exit(unit(sys.argv[2], sys.argv[3]))
    if kind == 'sweep':
        sys.exit(sweep(sys.argv[2], Path(sys.argv[3]), sys.argv[4], int(sys.argv[5])))
    head, full = sys.argv[2], Path(sys.argv[3])
    sys.exit(lane(head, full, sys.argv[4]) if kind == 'lane' else firmware(head, full))
