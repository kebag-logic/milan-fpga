#!/usr/bin/env python3
"""Compare a hosted run's per-worker measured span and per-suite windows with
the selector's predictions. Reviewer tool; reads the selector's tables by ast.

Usage: drift.py SELECTOR.py JOBS_META LOG...
JOBS_META lines: job<TAB>name<TAB>conclusion<TAB>startedAt<TAB>completedAt
"""
import ast
import math
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal

STAMP = re.compile(r"^[^\t]*\t[^\t]*\t\ufeff?(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?)Z (.*)$")


def ts(text):
    whole, _, frac = text.partition(".")
    base = datetime.strptime(whole, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    return Decimal(int(base.timestamp())) + (Decimal("0." + frac) if frac else 0)


def tables(path):
    out = {}
    for node in ast.parse(open(path, encoding="utf-8").read()).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("SUITE_SECONDS", "WORKER_OVERHEAD_SECONDS"):
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def main():
    selector, meta, *logs = sys.argv[1:]
    t = tables(selector)
    table, overhead = t["SUITE_SECONDS"], t["WORKER_OVERHEAD_SECONDS"]
    jobs = {}
    for line in open(meta):
        p = line.rstrip("\n").split("\t")
        jobs[p[0]] = p[1:]
    for path in logs:
        job = re.search(r"(\d+)\.log$", path).group(1)
        rows = [(ts(m.group(1)), m.group(2)) for line in open(path, encoding="utf-8")
                if (m := STAMP.match(line.rstrip("\n")))]
        k = next(i for i, (_, msg) in enumerate(rows) if msg.startswith("shard: "))
        idx = int(rows[k][1].split()[1].split("/")[0])
        prev = rows[k][0]
        windows = {}
        for when, msg in rows[k + 1:]:
            m = re.fullmatch(r"(PASS|FAIL|TIMEOUT) +(\S+).*", msg)
            if m:
                windows[m.group(2)] = (m.group(1), when - prev)
                prev = when
            if msg.startswith("suites: "):
                break
        predicted = overhead[idx] + sum(table[s] for s in windows)
        span = rows[-1][0] - rows[0][0]
        name, concl, start, end = jobs[job]
        jspan = (datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
                 - datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")).total_seconds()
        print(f"{name} ({concl}): predicted {predicted} s, job {jspan:.0f} s "
              f"({jspan / 60:.1f} min), log span {float(span):.0f} s, "
              f"ratio job/predicted {jspan / predicted:.3f}")
        for s, (v, w) in sorted(windows.items(), key=lambda kv: -table[kv[0]]):
            if table[s] >= 60:
                print(f"    {s:22} {v:7} table {table[s]:5} s  this run "
                      f"{math.ceil(w):5} s  ({float(w) / table[s] - 1:+.1%})")


if __name__ == "__main__":
    main()
