#!/usr/bin/env python3
"""R624-10: compare this review's unchanged runs of the 15 published review probes with the author's records.

usage: python3 -I compare_probe_outcomes.py <author r10 dir> <out.json> <name>=<results json> ...

For each probe, the author's `<name>-probe-rerun.json` holds the probe's own results file under 'results'. This
tool loads both, rewrites every absolute path to a placeholder, then compares, per case, the fields that carry
an outcome: exit status (exit/rc/observed_rc), verdict, and every line the check named (BAD, UNCOVERED, MARKUP),
whatever key the probe stores them under. A case is EQUAL when all of these match.
"""
import json
import re
import sys
from pathlib import Path

AUTH, OUT = Path(sys.argv[1]), Path(sys.argv[2])
PAIRS = [a.split("=", 1) for a in sys.argv[3:]]
PATH = re.compile(r"(?:/[\w.+@-]+)+/")
OUTCOME = ("exit", "rc", "observed_rc", "returncode", "verdict", "detected", "outcome", "status")


def norm(x):
    if isinstance(x, str):
        return PATH.sub("<path>/", x)
    if isinstance(x, list):
        return [norm(v) for v in x]
    if isinstance(x, dict):
        return {k: norm(v) for k, v in x.items()}
    return x


def cases(res):
    """A probe's case list, keyed by its name."""
    if isinstance(res, dict):
        for k in ("results", "cases", "probes", "forms"):
            if isinstance(res.get(k), list):
                return cases(res[k])
        return {"<whole>": res}
    out = {}
    for i, c in enumerate(res):
        if isinstance(c, dict):
            key = next((str(c[k]) for k in ("case", "name", "probe", "id", "form") if k in c), str(i))
            out[key] = c
        else:
            out[str(i)] = c
    return out


def named(c):
    s = json.dumps(c)
    return sorted(set(re.findall(r"(?:BAD|UNCOVERED|MARKUP) [^\"\\]*", s)))


def outcome(c):
    if not isinstance(c, dict):
        return {"value": c}
    return {k: c[k] for k in OUTCOME if k in c}


def main():
    report = []
    for name, mine in PAIRS:
        a = json.loads((AUTH / f"{name}-probe-rerun.json").read_text())
        ca, cm = cases(norm(a["results"])), cases(norm(json.loads(Path(mine).read_text())))
        rows = []
        for k in sorted(set(ca) | set(cm)):
            x, y = ca.get(k), cm.get(k)
            if x is None or y is None:
                rows.append(dict(case=k, equal=False, why="missing on one side"))
                continue
            eq = outcome(x) == outcome(y) and named(x) == named(y)
            rows.append(dict(case=k, equal=eq, outcome=outcome(y),
                             **({} if eq else dict(author=outcome(x), author_named=named(x), mine_named=named(y)))))
        report.append(dict(probe=name, author_exit=a["exit"], cases=len(rows),
                           equal=sum(r["equal"] for r in rows), rows=rows))
        print(name, "author exit", a["exit"], "cases", len(rows), "equal", sum(r["equal"] for r in rows))
    OUT.write_text(json.dumps(report, indent=1) + "\n")


if __name__ == "__main__":
    main()
