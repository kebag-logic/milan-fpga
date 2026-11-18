#!/usr/bin/env python3
"""attr.py LABEL...: decision 3's attribution at each head's legs (run_head.sh), cycles and committed instructions.

For each head (attr/b/LABEL), from its legs' logs and the scratch instruction files (<group>.txt.instr, patch_sim.py):
  record  aecp-largest-notice's records (aecp_mbx:frame spans, record_classes.py's): the dearest, and the other of
          the REMOVE/ADD pair, cycles and instructions;
  events  event.AECP (TIMER#3), event.MAAP (TIMER#2), AS_PATH_CHANGED, AVB_INFO_CHANGED: the dearest by cycles over
          the head's groups, by eventcost.py's own costs() (read-only copy of #665 round 28's tool), and the same
          event's instructions, its take to the next take (or the pass's first service_rx) less the TICK dispatch
          spans inside, as eventcost.py takes the cycles;
  rule    each cycle figure by the rule (cycles at 100 MHz, + 5 %, up to 5 us).
Writes attr/out/LABEL.json and prints one table row per head."""
import bisect
import json
import math
import sys
from pathlib import Path

T = Path('<scratch>')
sys.path.insert(0, str(T / 'tools/survey'))
import eventcost  # noqa: E402

KINDS = {'TIMER#3': 'event.AECP', 'TIMER#2': 'event.MAAP', 'AS_PATH_CHANGED': 'AS_PATH_CHANGED',
         'AVB_INFO_CHANGED': 'AVB_INFO_CHANGED'}


def rule(cycles: int) -> int:
    return int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)


def instr_of(path: Path):
    calls, spans = {}, {}
    for line in open(path, errors='replace'):
        f = line.split()
        if len(f) == 4 and f[0] == 'C':
            calls[(f[3], int(f[1]))] = int(f[2])
        elif len(f) == 5 and f[0] == 'S':
            spans.setdefault(f[4], {})[int(f[1])] = (int(f[2]), int(f[3]))
    return calls, spans


def event_costs(log: Path):
    """eventcost.costs(log), each event with its instructions: (kind, cycles, instructions)."""
    calls, spans = instr_of(Path(str(log)[:-4] + '.txt.instr'))
    written, passes, takes, rx, ticks = eventcost.events_of(log)
    tick_at = [s for s, _ in ticks]
    tick_instr = spans.get('ctrl_loop:dispatch_ticks', {})
    out, taken = [], 0
    for start, cycles in passes:
        end = start + cycles
        first_rx = rx[bisect.bisect_left(rx, start):bisect.bisect_left(rx, end)]
        if not first_rx:
            continue
        stop = first_rx[0]
        mine = takes[bisect.bisect_left(takes, start):bisect.bisect_left(takes, stop)]
        got = len(mine) if len(mine) == 8 else len(mine) - 1
        for k in range(max(got, 0)):
            a, b = mine[k], (mine[k + 1] if k + 1 < len(mine) else stop)
            lo, hi = bisect.bisect_left(tick_at, a), bisect.bisect_left(tick_at, b)
            spent = b - a - sum(d for _, d in ticks[lo:hi])
            ia = calls[('mbx_event_take', a)]
            ib = calls[('mbx_event_take', b)] if k + 1 < len(mine) else calls[('ctrl_loop:service_rx', b)]
            ins = ib - ia - sum(tick_instr[s][1] for s, _ in ticks[lo:hi])
            if taken < len(written):
                kind, slot = written[taken]
                out.append((eventcost.TYPES.get(kind, str(kind)) + (f'#{slot}' if kind == 1 else ''), spent, ins))
            taken += 1
    # the cycles are eventcost.py's own, event for event
    assert [(k, c) for k, c, _ in out] == eventcost.costs(log), log
    return out


def records(log: Path):
    _, spans = instr_of(Path(str(log)[:-4] + '.txt.instr'))
    frame = spans.get('aecp_mbx:frame', {})
    out = []
    for line in open(log, errors='replace'):
        f = line.split()
        if len(f) > 4 and f[0] == 'SPAN' and f[-1] == 'aecp_mbx:frame':
            start, cycles = int(f[2]), int(f[3])
            c, i = frame[start]
            assert c == cycles, (log, start)
            out.append((cycles, i, start))
    return out


def pass_of(log: Path, at: int) -> dict:
    """The pass holding the record that starts at CPU cycle `at`: its cycles, committed instructions and the
    instruction fetches it refilled from rom with their wait cycles (sim_main.cpp's PASS line)."""
    for line in open(log, errors='replace'):
        if not line.startswith('PASS '):
            continue
        f = line.split()
        start, cycles = int(f[3]), int(f[4])
        if start <= at < start + cycles:
            kv = dict(x.split('=', 1) for x in line.split(' W', 1)[0].split()[5:] if '=' in x)
            refills, wait = (int(v) for v in kv.get('fetch_rom', '0/0').split('/'))
            return {'pass_cycles': cycles, 'pass_instr': int(kv.get('instr', 0)), 'pass_refills': refills,
                    'pass_fetch_wait': wait}
    return {}


def head(label: str) -> dict:
    b = T / 'attr/b' / label
    res = {'label': label}
    long = b / 'none/part0/aecp-largest-notice.log'
    if long.is_file() and 'RESULT' in long.read_text(errors='replace')[-4000:]:
        recs = sorted(records(long), reverse=True)
        res['record'] = [{'cycles': c, 'instr': i, 'us': rule(c), 'cpi': round(c / i, 3), **pass_of(long, at)}
                         for c, i, at in recs[:2]]
    ev = {}
    for log in sorted(b.glob('*/part0/*.log')):
        if not log.with_suffix('.txt.instr').exists() and not Path(str(log)[:-4] + '.txt.instr').exists():
            continue
        if 'RESULT' not in log.read_text(errors='replace')[-4000:]:
            continue
        for kind, cycles, ins in event_costs(log):
            if kind in KINDS and (kind not in ev or cycles > ev[kind]['cycles']):
                ev[kind] = {'cycles': cycles, 'instr': ins, 'us': rule(cycles), 'cpi': round(cycles / ins, 3),
                            'where': f'{log.parent.parent.name}/{log.stem}'}
    res['events'] = {KINDS[k]: v for k, v in ev.items()}
    return res


def main():
    out = T / 'attr/out'
    out.mkdir(exist_ok=True)
    for label in sys.argv[1:]:
        r = head(label)
        (out / f'{label}.json').write_text(json.dumps(r, indent=1))
        rec = r.get('record', [{}])[0]
        cells = [f"rec {rec.get('cycles', '-')}c/{rec.get('instr', '-')}i"]
        for name in KINDS.values():
            e = r['events'].get(name, {})
            cells.append(f"{name} {e.get('cycles', '-')}c/{e.get('instr', '-')}i")
        print(label, ' | '.join(cells))


if __name__ == '__main__':
    main()
