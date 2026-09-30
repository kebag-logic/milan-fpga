#!/usr/bin/env python3
"""Is W6 (armed bound without the UART allowance) stricter or more lenient
than the head rule? One synthetic duty that starts before arming, carries a
10 ms UART allowance, and has a 245 ms armed opportunity-free lead.
Usage: w6_direction.py <head run.py> <W6 run.py>"""
import importlib.util, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.path.insert(0, str(__import__('pathlib').Path(path).parent))
    spec.loader.exec_module(mod); return mod
raw = ('BACKING armed=1 unbacked_cycles=0\n'
       'PHY_TIMING transactions=8 publications=1 max_transaction_cycles=10 '
       'max_poll_cycles=90 down_edges=1 up_edges=1\n')
for label, path in (("head", sys.argv[1]), ("W6", sys.argv[2])):
    m = load(path, "run_" + label)
    armed_at = 100_000_000
    blocks = [dict(kind='ticks', cycle=armed_at + 10, first=armed_at, last=armed_at, count=1, max_gap=0, gap_start=0),
              dict(kind='ticks', cycle=armed_at + 24_600_000, first=armed_at + 24_500_000,
                   last=armed_at + 24_500_000, count=1, max_gap=0, gap_start=0)]
    row = dict(m.interval('milan_status', armed_at - 1_000_000, armed_at + 24_600_000, None), uart_tx_allowance_ms=10.0)
    row.update(m.tick_span(blocks, row['start_sys_cycle'], row['end_sys_cycle']))
    row['period_bound_ms'] = 250 + row['no_tick_ms'] + 10.0
    got = m.service_findings(dict(rows=[row], media=dict(plan='all'), liveness=[dict(backed=1)], events=blocks), raw)
    print(f"{label}: armed_period_bound_ms={row.get('armed_period_bound_ms')} findings={got}")
