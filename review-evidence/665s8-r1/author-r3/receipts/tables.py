#!/usr/bin/env python3
"""tables.py <label>=<results.json>...: the README's Results tables from each run's results.json (scratch tool)."""
import json
import sys

PATHS = ('acmp.bind_rx', 'acmp.bind_to_probe_tx', 'acmp.probe_tx', 'acmp.probe_tx.entity', 'aecp.response',
         'aecp.response.get_avb_info', 'maap.egress', 'maap.probe_interval', 'maap.interval_error',
         'maap.announce_interval', 'adp.egress', 'adp.advertise_period', 'egress.acmp.first', 'egress.maap.first')


def cell(row):
    if row is None or not row['n']:
        return '-'
    if row['path'].startswith('egress.'):
        return f"{row['n']}: {row['min_us']:.2f} / {row['mean_us']:.2f} / {row['max_us']:.2f} us"
    return f"{row['n']}: {row['min_ms']:.3f} / {row['mean_ms']:.3f} / {row['max_ms']:.3f}"


def main():
    runs = [(a.split('=', 1)[0], json.load(open(a.split('=', 1)[1]))) for a in sys.argv[1:]]
    rows = {label: {r['path']: r for r in res['rows']} for label, res in runs}
    print('| Path (N: min / mean / max ms) | bound ms | ' + ' | '.join(label for label, _ in runs) + ' |')
    print('|---|---:|' + '---|' * len(runs))
    for path in PATHS:
        got = [rows[label].get(path) for label, _ in runs]
        if not any(g and g['n'] for g in got):
            continue
        bound = next((g['bound_ms'] for g in got if g), None)
        print(f"| `{path}` | {bound if bound is not None else '-'} | " + ' | '.join(cell(g) for g in got) + ' |')
    print()
    print('| Run | findings | censored | simulated ms | ready ms | load queued: offers (by an arm) / frames / echoes '
          'skipped | delivered: offers whole (in part) / frames | expiries met |')
    print('|---|---:|---|---:|---:|---|---|---|')
    for label, res in runs:
        load = res['load']
        q = ', '.join(f"{n} {t['queued_offers']} ({t['armed']}) / {t['queued_frames']} / {t['skipped']}"
                      for n, t in load.items()) or 'none'
        d = ', '.join(f"{n} {t['delivered_offers']} ({t['partial_offers']}) / {t['delivered_frames']}"
                      for n, t in load.items()) or 'none'
        m = ', '.join(f"{n} {t['expiries_met']}" for n, t in load.items() if t['armed']) or '-'
        print(f"| {label} | {len(res['findings'])} | {', '.join(res['censored']) or 'none'} | {res['simulated_ms']} | "
              f"{res['ready_ms']} | {q} | {d} | {m} |")
    print()
    for label, res in runs:
        delivered = sum(t['delivered_frames'] for t in res['load'].values())
        summary = dict(w.split('=', 1) for w in res['summary'].split()[1:])
        print(f"{label}: delivered {delivered} + 4 x {res['draws']} = {delivered + 4 * res['draws']}; "
              f"rx_frames {summary['rx_frames']} + bench_rx {summary['bench_rx']} = "
              f"{int(summary['rx_frames']) + int(summary['bench_rx'])}")
        for row in res['rows']:
            if row.get('strict_margin_ms') is not None:
                print(f"  {row['path']}: margin {row['margin_ms']} ms to {row['bound_ms']}, strict margin "
                      f"{row['strict_margin_ms']} ms to {row['strict_ms']}")


if __name__ == '__main__':
    main()
