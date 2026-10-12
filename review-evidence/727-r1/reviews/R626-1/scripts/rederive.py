#!/usr/bin/env python3
"""Independent re-derivation of the #727 duration tables from hosted logs.

Usage: python3 -I rederive.py HEAD_TREE BASE_SELECTOR DEV_LOG_DIR PR696_LOG JOBS_TXT

Parses each `gh run view --log` worker log without the selector's own
measure code: a timestamp is the third tab field (leading BOM stripped), read
as an exact Decimal. A suite's window runs from the previous verdict line (or
the `shard:` line) to its own verdict line; the worker's overhead is the log
span less its suite windows. Compares against the head's SUITE_SECONDS and
WORKER_OVERHEAD_SECONDS, re-checks the old hash split's in-sample model
against the API job durations, and prints predictions.
"""
import importlib.util
import math
import sys
from decimal import Decimal
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stamp(text):
    text = text.lstrip("﻿")
    date, clock = text.rstrip("Z").split("T")
    h, m, s = clock.split(":")
    y, mo, d = (int(x) for x in date.split("-"))
    # Days since epoch via proleptic ordinal, exact.
    import datetime
    days = datetime.date(y, mo, d).toordinal() - datetime.date(1970, 1, 1).toordinal()
    return Decimal(days * 86400 + int(h) * 3600 + int(m) * 60) + Decimal(s)


def parse(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        ts, _, msg = parts[2].partition(" ")
        try:
            t = stamp(ts)
        except Exception:
            continue
        rows.append((t, msg))
    first, last = rows[0][0], rows[-1][0]
    shard = None
    verdicts = []
    summary = None
    for t, msg in rows:
        if shard is None:
            if msg.startswith("shard: "):
                f = msg.split()
                idx, tot = (int(x) for x in f[1].split("/"))
                shard = (t, idx, tot, int(f[-1]))
            continue
        if summary is None:
            w = msg.split()
            if w and w[0] in ("PASS", "FAIL", "TIMEOUT") and len(w) >= 2:
                verdicts.append((t, w[0], w[1]))
            elif msg.startswith("suites: "):
                summary = t
    windows = {}
    prev = shard[0]
    for t, verdict, suite in verdicts:
        windows[suite] = (t - prev, verdict)
        prev = t
    overhead = None
    if summary is not None:
        overhead = (shard[0] - first) + (last - prev)
    return shard, windows, overhead, first, last


def ceil(d):
    return math.ceil(d)


def main(argv):
    head, base, devdir, pr696, jobs_txt = argv[1:6]
    hs = load(head, "head_selector")
    bs = load(base, "base_selector")
    api = {}
    for line in Path(jobs_txt).read_text().splitlines():
        f = line.split("\t")
        if len(f) == 6 and f[1].startswith("Verilator shard"):
            api.setdefault(f[0], (f[1], f[2], int(f[5])))
    measured, overhead, raw = {}, {}, {}
    worker_api = {}
    for log in sorted(Path(devdir).glob("*.log")):
        shard, windows, ovh, first, last = parse(log)
        _, idx, tot, sel = shard
        assert tot == 5 and len(windows) == sel, (log, sel, len(windows))
        assert all(v == "PASS" for _, v in windows.values())
        for suite, (d, _) in windows.items():
            raw[suite] = d
            measured[suite] = ceil(d)
        overhead[idx] = ceil(ovh)
        worker_api[idx] = api[log.stem][2]
        print(f"dev worker {idx}/5 job {log.stem}: {sel} suites, log span "
              f"{last - first} s, overhead {ovh} s -> {ceil(ovh)}, api {api[log.stem][2]} s")
    shard, windows, ovh, *_ = parse(pr696)
    d, v = windows["maap"]
    print(f"#696 worker {shard[1]}/{shard[2]} maap window {d} s ({v}) -> {ceil(d)}; "
          f"overhead {'n/a (cut off)' if ovh is None else ovh}")
    maap696 = ceil(d)
    print()
    table = dict(hs.SUITE_SECONDS)
    diffs = []
    for suite in sorted(set(table) | set(measured)):
        want = maap696 if suite == "maap" else measured.get(suite)
        if table.get(suite) != want:
            diffs.append((suite, table.get(suite), want))
    print(f"SUITE_SECONDS entries: {len(table)}; dev-measured suites: {len(measured)}")
    print(f"SUITE_SECONDS mismatches vs independent derivation "
          f"(maap from #696): {diffs or 'none'}")
    ov = tuple(overhead[i] for i in range(5))
    print(f"WORKER_OVERHEAD_SECONDS head {hs.WORKER_OVERHEAD_SECONDS} vs derived {ov}: "
          f"{'EQUAL' if ov == tuple(hs.WORKER_OVERHEAD_SECONDS) else 'DIFFER'}")
    print(f"dev maap window {raw['maap']} s -> {measured['maap']}")
    print()
    inv = sorted(table)
    # Old hash split, base selector, five workers.
    print("old hash split (base selector) predicted vs measured on dev run (in-sample):")
    for w in range(5):
        suites = bs.select_suites(inv, w, 5)
        pred = ov[w] + sum(measured[s] for s in suites)
        with696 = ov[w] + sum((maap696 if s == "maap" else measured[s]) for s in suites)
        print(f"  {w}/5 predicted {pred} s ({pred/60:.1f} min) api {worker_api[w]} s "
              f"({worker_api[w]/60:.1f} min) diff {pred - worker_api[w]:+d} s; "
              f"with #696 maap {with696} s ({with696/60:.1f} min)")
    print()
    print("new split predictions:")
    owners, loadv = hs.balance(inv, 5)
    for w in range(5):
        mine = [s for s in inv if owners[s] == w]
        own = ov[w] + sum(table[s] for s in mine)
        print(f"  {w}/5 {len(mine)} suites, predicted {own} s ({own/60:.1f} min), "
              f"selector says {loadv[w]}")
    for alt in (1380,):
        _, l2 = hs.balance(inv, 5, {**table, "maap": alt})
        print(f"  sensitivity maap={alt}: {l2} max {max(l2)} vs bound "
              f"{hs.bound_seconds(120)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
