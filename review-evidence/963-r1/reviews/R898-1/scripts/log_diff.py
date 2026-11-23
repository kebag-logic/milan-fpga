#!/usr/bin/env python3
"""Differential of two CPU service-budget harness group logs (base, head), nothing masked but time.

For each observable line kind, the sequence of lines in log order with the leading timestamp removed is compared:
WIRE (every wire frame: interface, channel, bytes), EVW (publication writes), TXC (TX counts), RXS/RXE/RXC
(the stimulus' receive records), MARK, ENTRY, PARTICIPANT, RESULT:. Also each probe's verdicts in the group's json
(status, verdict and every non-timing key), when given.

Usage: log_diff.py <base.log> <head.log> [<base.json> <head.json>]
"""
import json
import sys

KINDS = ('WIRE', 'EVW', 'TXC', 'RXS', 'RXE', 'RXC', 'MARK', 'ENTRY', 'PARTICIPANT', 'RESULT:')
TIMED = {'WIRE', 'EVW', 'TXC', 'RXS', 'RXE', 'RXC', 'MARK', 'ENTRY', 'PARTICIPANT'}


def end(path):
    """The run's last simulated sys cycle (SUMMARY sys=)."""
    with open(path, errors='replace') as f:
        for raw in f:
            if raw.startswith('SUMMARY '):
                return int(raw.split('sys=')[1].split()[0])
    return None


def lines(path, until=None):
    out = {k: [] for k in KINDS}
    with open(path, errors='replace') as f:
        for raw in f:
            parts = raw.rstrip('\n').split(' ')
            if parts and parts[0] in out:
                if until is not None and parts[0] == 'EVW' and int(parts[1]) > until:
                    continue
                out[parts[0]].append(' '.join(parts[2:] if parts[0] in TIMED else parts[1:]))
    return out


def main():
    eb, eh = end(sys.argv[1]), end(sys.argv[2])
    common = min(eb, eh)
    rb, rh = lines(sys.argv[1]), lines(sys.argv[2])
    print(f'run ends (sys): base {eb}, head {eh}; the testbench stimulus writes (EVW) compared up to {common}; '
          f'raw EVW counts base {len(rb["EVW"])}, head {len(rh["EVW"])}')
    base, head = lines(sys.argv[1], common), lines(sys.argv[2], common)
    same = True
    for k in KINDS:
        b, h = base[k], head[k]
        first = next((i for i, (x, y) in enumerate(zip(b, h)) if x != y), None)
        ok = b == h
        same &= ok
        print(f'{k:12} base {len(b):6} head {len(h):6} {"identical" if ok else "DIFFER"}'
              + ('' if ok else f' (first at {first if first is not None else min(len(b), len(h))})'))
    if base['ENTRY'] != head['ENTRY']:
        # ENTRY is the testbench's function-entry trace; a per-pass poll's entries count the passes, which a cut that
        # shortens passes changes. Reported apart, every other entry compared in order.
        poll = 'completion_source'
        b = [x for x in base['ENTRY'] if x != poll]
        h = [x for x in head['ENTRY'] if x != poll]
        print(f'ENTRY without the per-pass poll {poll!r}: base {len(b)} head {len(h)} '
              f'{"identical" if b == h else "DIFFER"}; {poll}: base {len(base["ENTRY"]) - len(b)} '
              f'head {len(head["ENTRY"]) - len(h)} (one a pass)')
    wire = sum(len(x) for x in base['WIRE'])
    print(f'wire frames: {len(base["WIRE"])}, {wire // 2} payload hex bytes compared')
    if len(sys.argv) > 4:
        jb, jh = json.load(open(sys.argv[3])), json.load(open(sys.argv[4]))

        keep = ('probe', 'row', 'family', 'interface', 'path', 'ring', 'ahead', 'budget_ms', 'ceiling_ms',
                'within_budget', 'within_ceiling', 'bound_within_budget', 'status')

        def verdicts(j):
            probes = [{k: p.get(k) for k in keep} | {'recipients': (p.get('fanout') or {}).get('recipients')}
                      for p in j['probes']]
            print(json.dumps(probes, sort_keys=True))
            return json.dumps(probes, sort_keys=True) + json.dumps(j.get('timeouts'), sort_keys=True)
        ok = verdicts(jb) == verdicts(jh)
        same &= ok
        print(f'probe verdicts (timing keys removed): {"identical" if ok else "DIFFER"}')
    print('RESULT:', 'IDENTICAL' if same else 'DIFFERENT')
    return 0 if same else 1


if __name__ == '__main__':
    sys.exit(main())
