#!/usr/bin/env python3
"""summary.py <results.json>...: the aggregate figures the README, the MAAP note and the PR quote (scratch tool)."""
import json
import sys


def rows(res, path):
    return [r for r in res['rows'] if r['path'] == path and r['n']]


def main():
    runs = [(p, json.load(open(p))) for p in sys.argv[1:]]
    agg = {}
    for _, res in runs:
        for r in res['rows']:
            if not r['n']:
                continue
            a = agg.setdefault(r['path'], dict(n=0, min=float('inf'), max=float('-inf'), bound=r['bound_ms'],
                                               strict=r.get('strict_ms')))
            a['n'] += r['n']
            a['min'] = min(a['min'], r['min_ms'])
            a['max'] = max(a['max'], r['max_ms'])
    for path in ('acmp.bind_rx', 'acmp.probe_tx', 'aecp.response', 'maap.egress', 'maap.probe_interval',
                 'maap.interval_error', 'maap.announce_interval', 'adp.egress', 'adp.advertise_period'):
        a = agg.get(path)
        if not a:
            continue
        extra = f", margin {a['bound'] - a['max']:.4f}" if a['bound'] is not None else ''
        extra += f", strict margin {a['strict'] - a['max']:.4f} to {a['strict']}" if a['strict'] else ''
        print(f"{path}: n {a['n']}, min {a['min']:.4f} ms, max {a['max']:.4f} ms{extra}")
    for p, res in runs:
        worst_acmp = max((r['max_ms'], r['path']) for r in res['rows'] if r['n'] and r['path'] in
                         ('acmp.bind_rx', 'acmp.probe_tx'))
        worst_aecp = max((r['max_ms'], r['path']) for r in res['rows'] if r['n'] and
                         r['path'].startswith('aecp.response.'))
        delivered = sum(t['delivered_frames'] for t in res['load'].values())
        summary = dict(w.split('=', 1) for w in res['summary'].split()[1:])
        print(f"{p}: findings {len(res['findings'])}, censored {res['censored']}, worst ACMP {worst_acmp}, worst AEM "
              f"{worst_aecp}; delivered {delivered} + 4 x {res['draws']} = {delivered + 4 * res['draws']} vs "
              f"{int(summary['rx_frames']) + int(summary['bench_rx'])}")


if __name__ == '__main__':
    main()
