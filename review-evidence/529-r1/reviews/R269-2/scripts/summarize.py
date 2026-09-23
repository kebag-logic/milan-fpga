#!/usr/bin/env python3
"""Tally reviewer mutant logs and grade each exchange at its own quadlets.

usage: summarize.py MUTDIR LOGDIR OUT.md
For every LOGDIR/<id>.<leg>.log: build and run exit, the harness tally, the count of
[FAIL] lines, and the [CTRS-CRF] / [NOTIFY-CRF] FAIL lines. For an exchange or
rotation mutant it also names which of the event arm's ten quadlet checks failed
and whether every moved port's own quadlet is among them.
"""
import glob
import os
import re
import sys

Q = {"cnt_locked": 0, "cnt_unlocked": 4, "cnt_intr": 8, "seq_err": 12, "mr_cnt": 16,
     "tu_cnt": 20, "fmt_err": 32, "late_cnt": 36, "early_cnt": 40, "pdu_count": 44}


def moved_ports(diff_text):
    return sorted({m.group(1) for m in re.finditer(r"^\+\s+\.(\w+)_o\s", diff_text, re.M)})


def main():
    mutdir, logdir, out = sys.argv[1:4]
    idx = {}
    if os.path.exists(os.path.join(mutdir, "index.tsv")):
        for ln in open(os.path.join(mutdir, "index.tsv")):
            p = ln.rstrip("\n").split("\t")
            idx[p[0]] = (p[1], p[2])
    rows, bad = [], []
    for log in sorted(glob.glob(os.path.join(logdir, "*.log"))):
        base = os.path.basename(log)[:-4]
        mid, leg = base.rsplit(".", 1)
        t = open(log, errors="replace").read()
        bexit = re.search(r"build_exit=(\d+)", t)
        rexit = re.search(r"run_exit=(\d+)", t)
        tally = re.search(r"checks: (\d+)\s+failures: (\d+)", t)
        fails = [ln.strip() for ln in t.splitlines() if "[FAIL]" in ln]
        crf = [f for f in fails if "[CTRS-CRF]" in f or "[NOTIFY-CRF]" in f]
        ev = sorted({int(m.group(1)) for f in fails
                     for m in [re.search(r"events, all ten: @(\d+) ", f)] if m})
        verdict = ("BUILD-FAIL" if bexit and bexit.group(1) != "0"
                   else "KILLED" if rexit and rexit.group(1) != "0"
                   else "SURVIVED" if rexit else "NO-RESULT")
        own = ""
        if mid.startswith(("vx-", "vr")) and os.path.exists(os.path.join(mutdir, mid, "mutant.diff")):
            ports = moved_ports(open(os.path.join(mutdir, mid, "mutant.diff")).read())
            need = sorted(Q[p] for p in ports)
            ok = all(q in ev for q in need)
            own = f"own quadlets {need} red: {'yes' if ok else 'NO'}"
            if not ok:
                bad.append(f"{mid}.{leg}")
        rows.append((mid, leg, idx.get(mid, ("base" if mid == "base" else "?", ""))[0],
                     verdict, tally.group(0) if tally else "-", len(fails), len(crf),
                     ",".join(f"@{q}" for q in ev) or "-", own,
                     crf[0][:150] if crf else (fails[0][:150] if fails else "")))
    with open(out, "w") as f:
        f.write("| mutant | leg | class | verdict | tally | FAIL lines | CRF-tagged FAIL | event-arm quadlets red | own quadlets | first CRF-tagged (else first) FAIL |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            f.write("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |\n")
        f.write(f"\nexchange/rotation logs missing an own-quadlet red: {len(bad)} {bad}\n")
    print(f"{len(rows)} logs; own-quadlet misses: {bad}")


if __name__ == "__main__":
    main()
