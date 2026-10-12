#!/usr/bin/env python3
"""Independent re-derivation of the #727 duration tables from hosted worker logs.

Written by the reviewer; it does not import scripts/suite_shards.py. Usage:
  remeasure.py SELECTOR.py JOBS_META LOG... [--extra-maap LOG]
Prints per-log windows, overhead, log span vs job span, and the comparison
against the selector's SUITE_SECONDS / WORKER_OVERHEAD_SECONDS (parsed with ast).
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
    return Decimal(int(base.timestamp())) + (Decimal("0." + frac) if frac else Decimal(0))


def iso(text):
    return Decimal(int(datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc).timestamp()))


def measure(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        m = STAMP.match(line.rstrip("\n"))
        if m:
            rows.append((ts(m.group(1)), m.group(2)))
    shard = next((i for i, (_, msg) in enumerate(rows)
                  if re.fullmatch(r"shard: \d+/\d+ +selected suites: \d+", msg)), None)
    s_t, s_msg = rows[shard]
    idx, tot, sel = map(int, re.findall(r"\d+", s_msg))
    results = []
    summary = None
    for t, msg in rows[shard + 1:]:
        m = re.fullmatch(r"(PASS|FAIL|TIMEOUT) +(\S+).*", msg)
        if m and summary is None:
            results.append((t, m.group(1), m.group(2)))
        elif msg.startswith("suites: ") and summary is None:
            summary = t
    windows = {}
    prev = s_t
    raw = {}
    for t, verdict, suite in results:
        raw[suite] = t - prev
        windows[suite] = math.ceil(t - prev)
        prev = t
    first, last = rows[0][0], rows[-1][0]
    overhead = math.ceil((s_t - first) + (last - prev)) if summary is not None else None
    return dict(index=idx, total=tot, selected=sel, n=len(results), windows=windows,
                raw=raw, overhead=overhead, span=last - first,
                verdicts={v for _, v, _ in results})


def table(selector):
    tree = ast.parse(open(selector, encoding="utf-8").read())
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if isinstance(target, ast.Name) and target.id in (
                    "SUITE_SECONDS", "WORKER_OVERHEAD_SECONDS"):
                out[target.id] = ast.literal_eval(node.value)
    return out


def main():
    selector, meta = sys.argv[1], sys.argv[2]
    rest = sys.argv[3:]
    extra = None
    if "--extra-maap" in rest:
        k = rest.index("--extra-maap")
        extra = rest[k + 1]
        rest = rest[:k] + rest[k + 2:]
    jobs = {}
    for line in open(meta):
        parts = line.rstrip("\n").split("\t")
        if len(parts) == 5:
            jobs[parts[0]] = (parts[1], parts[2], iso(parts[4]) - iso(parts[3]))
    committed = table(selector)
    seconds, overhead = {}, {}
    for path in rest:
        m = measure(path)
        job = re.search(r"(\d+)\.log$", path).group(1)
        name, concl, jspan = jobs[job]
        print(f"{name} job {job} {concl}: suites {m['n']}/{m['selected']} verdicts "
              f"{sorted(m['verdicts'])} overhead {m['overhead']} s, log span "
              f"{float(m['span']):.1f} s, job span {jspan} s "
              f"({float(jspan)/60:.2f} min), sum(windows)+overhead "
              f"{sum(m['windows'].values()) + m['overhead']} s")
        for suite, value in m["windows"].items():
            assert suite not in seconds, suite
            seconds[suite] = value
        overhead[m["index"]] = m["overhead"]
    if extra:
        m = measure(extra)
        print(f"#696 log: maap raw window {m['raw'].get('maap')} s -> "
              f"{m['windows'].get('maap')} s; dev maap {seconds.get('maap')} s")
        seconds["maap"] = m["windows"]["maap"]
    diffs = {s: (seconds.get(s), committed["SUITE_SECONDS"].get(s))
             for s in sorted(set(seconds) | set(committed["SUITE_SECONDS"]))
             if seconds.get(s) != committed["SUITE_SECONDS"].get(s)}
    ov = tuple(overhead[i] for i in sorted(overhead))
    print(f"suites measured {len(seconds)}, committed {len(committed['SUITE_SECONDS'])}")
    print(f"SUITE_SECONDS differences (measured, committed): {diffs or 'none'}")
    print(f"overhead measured {ov}, committed {committed['WORKER_OVERHEAD_SECONDS']}, "
          f"equal={ov == tuple(committed['WORKER_OVERHEAD_SECONDS'])}")
    return 0 if not diffs and ov == tuple(committed["WORKER_OVERHEAD_SECONDS"]) else 1


if __name__ == "__main__":
    sys.exit(main())
