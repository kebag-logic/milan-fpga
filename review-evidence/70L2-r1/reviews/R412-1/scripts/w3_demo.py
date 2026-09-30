#!/usr/bin/env python3
"""Concrete case for the surviving W3 rule: an ARMED command duty (it starts
after the writer's first heartbeat opportunity) whose first 400 ms carry no
opportunity. The head grader must refuse it; the W3 copy (arming read per
duty, from the first opportunity inside it) passes it.
usage: w3_demo.py <head run.py dir> <W3 run.py dir>"""
import importlib.util
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path + "/run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, path)
    spec.loader.exec_module(mod)
    return mod


for label, path in (("head", sys.argv[1]), ("W3", sys.argv[2])):
    m = load(path, "run_" + label)
    armed_at, start = 1_000_000, 50_000_000          # writer armed long before the duty
    first_inside, end = start + 40_000_000, start + 45_000_000   # 400 ms, then ticks
    row = dict(m.interval('milan_status', start, end, None), uart_tx_allowance_ms=0.0)
    events = [dict(kind='ticks', cycle=armed_at + 10, first=armed_at, last=armed_at, count=1,
                   max_gap=0, gap_start=0),
              dict(kind='ticks', cycle=end, first=first_inside, last=end - 100_000, count=50,
                   max_gap=100_000, gap_start=first_inside)]
    row.update(m.tick_span(events, start, end))
    row['period_bound_ms'] = 250 + row['no_tick_ms']
    result = dict(rows=[row], media=dict(plan='all'), liveness=[dict(backed=1)], events=events)
    findings = m.service_findings(result, "BACKING armed=1 unbacked_cycles=0\n"
                                  "PHY_TIMING transactions=8 publications=1 max_transaction_cycles=10 "
                                  "max_poll_cycles=90 down_edges=1 up_edges=1\n")
    print(f"{label}: no_tick_ms={row['no_tick_ms']:.3f} findings={findings}")
