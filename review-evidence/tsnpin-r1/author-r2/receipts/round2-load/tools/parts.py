#!/usr/bin/env python3
"""Each part of every pass of instrumented budget-harness logs (#665, round 21): the most each part took over every
measured instance, in CPU cycles, and its stated cost, that plus 5 % rounded up to 5 us (100 cycles a microsecond).

usage: python3 -I parts.py OUT.json RESULTS_DIR...

The legs' testbench reports, besides PASS lines, SPAN lines (entry to return) of ctrl_loop's dispatch_ticks and
round_of, srp_mbx's open_interface, receive and poll, aecp_mbx's frame and poll, adp_mbx's on_poll, acmp_mbx's
on_adp_frame, on_frame and on_poll, maap_mbx's receive and poll, the two ctrl_app deliver polls and nvm_store_service,
and CALL lines (entries) of mbx_event_take and ctrl_loop's service_rx, aecp_command and aecp's finish. Spans a leg did
not trace are absent from its parts. A pass is its PASS line's window. Only logs that end in a RESULT line are read.
  events:     from the pass's start to its first service_rx, less its dispatch_ticks spans (a pass's events and the
              drain mark and tick call around them); events_none: the same in a pass that took none
  polls:      from the first poll's entry (adp_mbx's on_poll) to the pass's end, its round's or its step's start,
              less its rebuild spans; polls_base: the same less AECP's poll where AECP's poll fanned a notice out
  records:    each channel's handler span (srp receive, aecp frame, acmp on_frame, adp via acmp on_adp_frame, maap
              receive)
"""
import bisect
import collections
import json
import math
import sys
from pathlib import Path

HANDLERS = {'srp': 'srp_mbx:receive', 'aecp': 'aecp_mbx:frame', 'acmp': 'acmp_mbx:on_frame',
            'adp': 'acmp_mbx:on_adp_frame', 'maap': 'maap_mbx:receive'}
POLLS = ('aecp_mbx:poll', 'srp_mbx:poll', 'maap_mbx:poll', 'acmp_mbx:on_poll', 'adp_mbx:on_poll',
         'ctrl_app_aecp:deliver', 'ctrl_app_srp:deliver')


def stated(cycles: int) -> int:
    """The stated cost of a most-measured figure: plus 5 %, rounded up to 5 us."""
    return int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)


AECP_CH = 2


def parse(path: Path):
    passes, calls, spans = [], collections.defaultdict(list), collections.defaultdict(list)
    sysspans, aecp_tx = collections.defaultdict(list), []
    parse.any_tx, parse.passes_sys = [], {}
    for line in open(path, errors='replace'):
        f = line.split()
        if not f:
            continue
        if f[0] == 'PASS':
            passes.append((int(f[3]), int(f[4])))
            parse.passes_sys[int(f[3])] = int(f[2])
        elif f[0] == 'CALL':
            calls[f[3]].append(int(f[2]))
        elif f[0] == 'SPAN':
            spans[f[5]].append((int(f[2]), int(f[3])))
            sysspans[f[5]].append((int(f[1]), int(f[3])))
        elif f[0] == 'TXC':
            parse.any_tx.append(int(f[1]))
            if int(f[2]) == AECP_CH:
                aecp_tx.append(int(f[1]))
    for v in list(calls.values()) + list(spans.values()) + [aecp_tx, parse.any_tx]:
        v.sort()
    parse.sysspans, parse.aecp_tx = sysspans, aecp_tx
    return passes, calls, spans


def inside(values, a, b):
    return values[bisect.bisect_left(values, a):bisect.bisect_left(values, b)]


_KEYS = {}


def spans_in(spans, a, b):
    """The spans (start, cycles), sorted by start, that start in [a, b); each list's starts indexed once."""
    keys = _KEYS.get(id(spans))
    if keys is None or len(keys) != len(spans):
        keys = _KEYS[id(spans)] = [s for s, _ in spans]
    return spans[bisect.bisect_left(keys, a):bisect.bisect_left(keys, b)]


def main():
    out_path, dirs = Path(sys.argv[1]), sys.argv[2:]
    most = collections.defaultdict(int)
    least = {}
    where = {}
    counts = collections.Counter()
    logs = 0

    def note(key, cycles, log, start):
        counts[key] += 1
        if cycles > most[key]:
            most[key], where[key] = cycles, (log, start)

    for d in dirs:
        for path in sorted(Path(d).glob('*.log')):
            text = path.read_text(errors='replace')
            if 'RESULT' not in text[-4000:]:
                continue
            logs += 1
            _KEYS.clear()
            passes, calls, spans = parse(path)
            name = f'{Path(d).parent.name}/{path.name}'
            for ch, label in HANDLERS.items():
                for start, cycles in spans.get(label, []):
                    note(f'record.{ch}', cycles, name, start)
            for start, cycles in spans.get('ctrl_loop:round_of', []):
                note('round', cycles, name, start)
            for start, cycles in spans.get('srp_mbx:open_interface', []):
                note('rebuild', cycles, name, start)
            for start, cycles in spans.get('ctrl_loop:dispatch_ticks', []):
                if cycles > 1000:
                    note('centisecond_consumers', cycles, name, start)
            for p in POLLS:
                for (s_sys, cycles), (start, _) in zip(parse.sysspans.get(p, []), spans.get(p, [])):
                    note(f'poll.{p}', cycles, name, start)
                    # a poll that committed no frame on any channel and rebuilt no interface: the polls' base every
                    # pass pays; one that did is an arrival's (an owed frame, a rebuild after a link change)
                    rebuilt = spans_in(spans.get('srp_mbx:open_interface', []), start, start + cycles)
                    if rebuilt:
                        note(f'poll_rebuilding.{p}', cycles, name, start)
                    elif not inside(parse.any_tx, s_sys, s_sys + cycles):
                        note(f'poll_idle.{p}', cycles, name, start)
                    else:
                        note(f'poll_sending.{p}', cycles, name, start)
            # AECP's poll that committed no AECP frame (its base) and one that sent (an owed response, a completed
            # apply's response and notification, a probe or a notice's fan-out continued)
            for (s_sys, cycles), (start, _) in zip(parse.sysspans.get('aecp_mbx:poll', []), spans.get('aecp_mbx:poll', [])):
                sent = inside(parse.aecp_tx, s_sys, s_sys + cycles)
                note('poll.aecp_sending' if sent else 'poll.aecp_idle', cycles, name, start)
                if len(sent) == 1:
                    note('poll.aecp_one_frame', cycles, name, start)
            passes_sys = parse.passes_sys
            for start, cycles in passes:
                end = start + cycles
                rx = inside(calls.get('ctrl_loop:service_rx', []), start, end)
                if rx:
                    ticks = spans_in(spans.get('ctrl_loop:dispatch_ticks', []), start, rx[0])
                    takes = len(inside(calls.get('mbx_event_take', []), start, rx[0]))
                    events = rx[0] - start - sum(c for _, c in ticks)
                    note('events' if takes > 1 else 'events_none', events, name, start)
                    note(f'events.taken{min(takes - 1, 8) if takes < 8 else 8}', events, name, start)
                first = spans_in(spans.get('adp_mbx:on_poll', []), start, end)
                if first:
                    a = first[0][0]
                    stops = [s for s, _ in spans_in(spans.get('ctrl_loop:round_of', []), a, end)] + \
                            [s for s, _ in spans_in(spans.get('nvm_store_service', []), a, end)]
                    stop = min(stops) if stops else end
                    rebuild = sum(c for _, c in spans_in(spans.get('srp_mbx:open_interface', []), a, stop))
                    aecp = sum(c for _, c in spans_in(spans.get('aecp_mbx:poll', []), a, stop))
                    polls = stop - a - rebuild
                    note('polls', polls, name, start)
                    if rx:
                        least['polls'] = min(least.get('polls', polls), polls)
                    # the whole polls section where no poll committed a frame and none rebuilt: the polls' base
                    a_sys = a - start + passes_sys.get(start, start)
                    if not rebuild and not inside(parse.any_tx, a_sys, a_sys + (stop - a)):
                        note('polls_idle', polls, name, start)
                    if 'aecp_mbx:poll' in spans:
                        note('polls_less_aecp', polls - aecp, name, start)
    result = dict(logs=logs, least_cycles=least, parts={k: dict(most_cycles=most[k], stated_us=stated(most[k]), instances=counts[k],
                                            where=where[k]) for k in sorted(most)})
    out_path.write_text(json.dumps(result, indent=1) + '\n')
    for k in sorted(most):
        print(f'{k:32} most {most[k]:>8,} cycles over {counts[k]:>7,} instances, stated {stated(most[k]):>5} us; '
              f'{where[k][0]}')


if __name__ == '__main__':
    main()
