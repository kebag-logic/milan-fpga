#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R458-2: compare the unchanged round-1 probe run at the head with the round-1
receipt, and name each probe's failing committed checks per shape.
usage: probe_receipt.py <round1 probe_results.txt> <work dir of this run>"""
import collections, pathlib, re, sys
r1 = {}
for ln in pathlib.Path(sys.argv[1]).read_text().splitlines():
    p = ln.split("\t")
    if len(p) == 3 and p[0] != "probe" and not ln.startswith("#"):
        r1[(p[0], p[1])] = p[2]
work = pathlib.Path(sys.argv[2])
now = {}
for ln in (work / "probe_results.tsv").read_text().splitlines()[1:]:
    a, b, c = ln.split("\t")
    now[(a, b)] = c
print("# unchanged round-1 probes.py at head 9160f7d7 (scripts byte-identical to R458-1's MANIFEST)")
print("# committed suite cell = rc of default `make` (0 = probe survives); lockstep cells as in round 1")
print("probe\trun\tround1(65324390)\tnow(9160f7d7)\tlockstep-equal")
for k in sorted(set(r1) | set(now)):
    same = "" if k[1] in ("srp_top", "srp_stream_fsms", "srp_admission") else ("yes" if r1.get(k) == now.get(k) else "NO")
    print(f"{k[0]}\t{k[1]}\t{r1.get(k,'-')}\t{now.get(k,'-')}\t{same}")
print()
print("# per probe: caught by which committed suite; failing checks by tag and [sources/sinks] shape")
probes = sorted({k[0] for k in now})
uncaught = []
for p in probes:
    caught = [s for (q, s), v in now.items() if q == p and s in ("srp_top", "srp_stream_fsms", "srp_admission") and v != "0"]
    if not caught:
        uncaught.append(p)
    for s in ("srp_top", "srp_stream_fsms", "srp_admission"):
        log = work / p / f"suite-{s}.log"
        if not log.exists():
            continue
        txt = log.read_text()
        fails = [l for l in txt.splitlines() if l.startswith("FAIL:")]
        tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", txt)
        per = collections.Counter()
        for l in fails:
            tag = l.split(":", 2)[1].strip().split(" ")[0]
            m = re.search(r"\[(\d+/\d+)\]\s*$", l)
            per[(tag, m.group(1) if m else "8-ctx suite")] += 1
        cells = ", ".join(f"{t}@{sh} x{n}" for (t, sh), n in sorted(per.items()))
        print(f"{p}\t{s}\trc={now.get((p, s), '-')}\ttallies={' | '.join(tally)}\tfails={len(fails)}\t{cells}")
print()
print(f"probes: {len(probes)}; caught by a committed suite: {len(probes) - len(uncaught)}; uncaught: {uncaught}")
