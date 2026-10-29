#!/usr/bin/env python3
"""Scratch: the profiling variant's CALLS lines (a helper's own cycles, by the function that entered it), summed
over a composed row's window (prof.py's window and counted passes).

usage: calls.py [--top N] LABEL=RESULTS_DIR ..."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prof  # noqa: E402


def calls(log: Path) -> dict[int, dict[str, tuple[int, int]]]:
    out = {}
    for line in log.read_text().splitlines():
        if line.startswith('CALLS '):
            f = line.split()
            out[int(f[1])] = {kv.rpartition('=')[0]: tuple(int(x) for x in kv.rpartition('=')[2].split('/'))
                              for kv in f[2:]}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=12)
    ap.add_argument('runs', nargs='+')
    args = ap.parse_args()
    for spec in args.runs:
        label, _, path = spec.partition('=')
        results = Path(path)
        cpu_hz = json.loads((results.parent / 'soc.json').read_text())['cpu_hz']
        for group in prof.GROUPS:
            log = results / f'{group}.log'
            res = json.loads((results / f'{group}.json').read_text())
            per_pass = calls(log)
            sys_hz = json.loads((results.parent / 'soc.json').read_text())['sys_hz']
            for row, name in prof.ROWS:
                w = prof.window(res, row)
                if w is None:
                    continue
                start, end, probe = w
                counted = [p for p in prof.passes(log)
                           if p['start'] < end and p['start'] + p['cycles'] * sys_hz / cpu_hz > start]
                total = Counter()
                for p in counted:
                    for k, (cyc, _) in per_pass.get(p['n'], {}).items():
                        total[k] += cyc
                print(f'\n#### {label} {group} `{probe}`\n')
                print('| Helper <- caller | ms |\n|---|---:|')
                for k, cyc in total.most_common(args.top):
                    print(f'| `{k}` | {cyc * 1000.0 / cpu_hz:.3f} |')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
