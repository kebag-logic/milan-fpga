#!/usr/bin/env python3
"""Scratch: what a composed row's window executes, from a profiling-variant harness log (FUNCS and ILINES lines).

usage: prof.py [--top N] [--json OUT] LABEL=RESULTS_DIR ...

For each backlog group and each of the rows the assignment names (the last AECP record and the last SRP record,
wherever the group places them), the window runs from the group's first loaded record's commit to the row's
release (round 5's decomp.py window). Every work pass that overlaps the window is counted whole (its PASS line
gives its start and its CPU cycles; the variant prints a FUNCS and an ILINES line after it). Per window:
- the window, the counted passes' cycles, and the part of the first pass that ran before the window;
- instruction-cache line refills: count, distinct lines, their wait (CPU cycles, command to last beat);
- data side: IO-bus waits (every uncached access, the mailbox's among them), data-cache line refills and the cycles
  one was outstanding, write-backs and the cycles one was outstanding;
- each function's own cycles (by committed PC), instructions and the refills of its own lines, top N by cycles.
All times in ms at the run's CPU clock (soc.json's cpu_hz)."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

GROUPS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')
ROWS = (('aecp', 'AECP record, last'), ('srp', 'SRP record, last'))
FIELDS = ('cycles', 'instr', 'irefills', 'irefill_wait', 'io_wait', 'drefills', 'dbusy', 'dwrites', 'dwbusy')


def passes(log: Path) -> list[dict]:
    """Every work pass: its start (bus cycles), CPU cycles, and the variant's per-function costs and refill lines."""
    out = []
    for line in log.read_text().splitlines():
        if line.startswith('PASS '):
            f = line.split()
            out.append(dict(n=int(f[1]), start=int(f[2]), cycles=int(f[4]), funcs={}, lines=[]))
        elif line.startswith('FUNCS '):
            f = line.split()
            assert out and out[-1]['n'] == int(f[1]), line[:80]
            for kv in f[2:]:
                name, _, v = kv.rpartition('=')
                out[-1]['funcs'][name] = tuple(int(x) for x in v.split('/'))
        elif line.startswith('ILINES '):
            f = line.split()
            assert out and out[-1]['n'] == int(f[1]), line[:80]
            out[-1]['lines'] = [int(x, 16) for x in f[2:]]
    return out


def window(res: dict, path: str) -> tuple[int, int, str] | None:
    """The window of the group's last record of a path: (start, end, probe), or None when it has none."""
    service = [p for p in res['probes'] if '.service.' in p['probe'] and p.get('end_sys')]
    if not service:
        return None
    start = min(p['start_sys'] for p in service)
    row = [p for p in service if f'.service.{path}.last.' in p['probe']]
    if not row:
        return None
    return start, row[0]['end_sys'], row[0]['probe']


def analyse(results: Path, group: str, path: str, top: int) -> dict | None:
    res = json.loads((results / f'{group}.json').read_text())
    w = window(res, path)
    if w is None:
        return None
    start, end, probe = w
    spec = json.loads((results.parent / 'soc.json').read_text())
    sys_hz, cpu_hz = spec['sys_hz'], spec['cpu_hz']
    ms_cpu = lambda c: c * 1000.0 / cpu_hz
    ms_sys = lambda c: c * 1000.0 / sys_hz
    counted = [p for p in passes(results / f'{group}.log')
               if p['start'] < end and p['start'] + p['cycles'] * sys_hz / cpu_hz > start]
    total = defaultdict(lambda: [0] * len(FIELDS))
    lines = Counter()
    for p in counted:
        for name, v in p['funcs'].items():
            t = total[name]
            for k, x in enumerate(v):
                t[k] += x
        lines.update(p['lines'])
    sums = [sum(t[k] for t in total.values()) for k in range(len(FIELDS))]
    before = max(0.0, ms_sys(start - counted[0]['start'])) if counted else 0.0
    funcs = sorted(total.items(), key=lambda kv: -kv[1][0])
    return dict(group=group, probe=probe, window_ms=ms_sys(end - start), passes=len(counted),
                pass_ms=ms_cpu(sum(p['cycles'] for p in counted)), before_ms=before,
                instr=sums[1], irefills=sums[2], ilines=len(lines), irefill_ms=ms_cpu(sums[3]),
                io_ms=ms_cpu(sums[4]), drefills=sums[5], dbusy_ms=ms_cpu(sums[6]), dwrites=sums[7],
                dwbusy_ms=ms_cpu(sums[8]),
                funcs=[dict(name=n, ms=ms_cpu(v[0]), instr=v[1], irefills=v[2], irefill_ms=ms_cpu(v[3]),
                            io_ms=ms_cpu(v[4]), drefills=v[5]) for n, v in funcs],
                hot_lines=lines.most_common(), top=top)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=25)
    ap.add_argument('--json', type=Path)
    ap.add_argument('runs', nargs='+')
    args = ap.parse_args()
    every = []
    for spec in args.runs:
        label, _, path = spec.partition('=')
        for group in GROUPS:
            for row, _ in ROWS:
                r = analyse(Path(path), group, row, args.top)
                if r:
                    r['label'] = label
                    every.append(r)
    print('| Run | Group | Row | Window, ms | Passes (ms; before the window) | Instructions | I$ refills (lines) | '
          'I$ refill wait, ms | IO waits, ms | D$ refills (outstanding, ms) | D$ write-backs (outstanding, ms) |')
    print('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for r in every:
        print(f"| {r['label']} | {r['group']} | `{r['probe']}` | {r['window_ms']:.2f} | {r['passes']} "
              f"({r['pass_ms']:.2f}; {r['before_ms']:.2f}) | {r['instr']:,} | {r['irefills']:,} ({r['ilines']:,}) | "
              f"{r['irefill_ms']:.2f} | {r['io_ms']:.2f} | {r['drefills']:,} ({r['dbusy_ms']:.2f}) | "
              f"{r['dwrites']:,} ({r['dwbusy_ms']:.2f}) |")
    for r in every:
        print(f"\n#### {r['label']} {r['group']} `{r['probe']}`: window {r['window_ms']:.2f} ms\n")
        print('| Function | Own cycles, ms | Instructions | I$ refills of its lines | Their wait, ms | IO waits, ms | '
              'D$ refills |')
        print('|---|---:|---:|---:|---:|---:|---:|')
        for f in r['funcs'][:args.top]:
            print(f"| `{f['name']}` | {f['ms']:.3f} | {f['instr']:,} | {f['irefills']:,} | {f['irefill_ms']:.3f} | "
                  f"{f['io_ms']:.3f} | {f['drefills']:,} |")
    if args.json:
        args.json.write_text(json.dumps(every, indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
