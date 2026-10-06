#!/usr/bin/env python3
"""Recompute #673 suite windows and per-shard job envelopes from hosted logs.

Usage: survey_envelope.py JOB_INDEX_TSV LOG_DIR SHARDS_TXT [--exclude-run RUN ...]

JOB_INDEX_TSV rows: run, '', job, name, status, conclusion, started, completed.
LOG_DIR holds log_<run>_<job>.txt (raw job logs from the Actions API).
SHARDS_TXT is `suite_shards.py` output at the head under review.

Window rule (as stated in PR #681): the first window opens at the
`shard: I/N` line, every later one at the previous verdict line, and each
closes at its own verdict timestamp.  Overhead = completed - started -
sum(windows), computed only for jobs whose verdict count equals the
selected-suite count.  TIMEOUT windows are cutoffs, not completions.
"""
import datetime as dt
import re
import sys
from collections import defaultdict

TS = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d+))?Z (.*)$")
SHARD = re.compile(r"^shard: (\d+)/(\d+)\s+selected suites: (\d+)")
VERDICT = re.compile(r"^(PASS|FAIL|TIMEOUT)\s+(\S+)")
NEW = {"capture_coherence": 2400, "milan_dp_mclk": 3600, "milan_dp": 4800}
OLD = {"milan_dp": 3600, "milan_dp_gptp": 5400}
JOB_TIMEOUT = 7200


def ts(date, frac):
    t = dt.datetime.fromisoformat(date).replace(tzinfo=dt.timezone.utc)
    return t.timestamp() + (float("0." + frac) if frac else 0.0)


def iso(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def parse(path):
    shard = None
    selected = None
    last = None
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = TS.match(line.rstrip("\n"))
        if not m:
            continue
        t, body = ts(m.group(1), m.group(2)), m.group(3)
        s = SHARD.match(body)
        if s:
            shard, selected, last = int(s.group(1)), int(s.group(3)), t
            continue
        v = VERDICT.match(body)
        if v and last is not None:
            out.append((v.group(2), v.group(1), t - last))
            last = t
    return shard, selected, out


def main(argv):
    index, logdir, shards_txt = argv[1:4]
    exclude = set(argv[argv.index("--exclude-run") + 1:]) if "--exclude-run" in argv else set()
    owner = {}
    cur = None
    for line in open(shards_txt):
        if line.startswith("== shard"):
            cur = int(line.split()[2].split("/")[0])
        elif cur is not None and line.strip():
            for s in line.split():
                owner[s] = cur
    best = defaultdict(lambda: (0.0, None, None))       # suite -> max PASS/FAIL window
    cut = defaultdict(lambda: (0.0, None, None))        # suite -> max TIMEOUT window
    ovh = defaultdict(lambda: (-1.0, None))             # shard -> max overhead
    total = defaultdict(lambda: (0.0, None))
    windows = 0
    mismatch = []
    for row in open(index):
        f = row.rstrip("\n").split("\t")
        run, job, name, concl, st, en = f[0], f[2], f[3], f[5], f[6], f[7]
        if concl == "skipped" or run in exclude or "Verilator shard" not in name:
            continue
        shard, selected, out = parse(f"{logdir}/log_{run}_{job}.txt")
        if shard is None:
            continue
        dur = iso(en) - iso(st)
        if dur > total[shard][0]:
            total[shard] = (dur, job)
        for suite, verdict, w in out:
            windows += 1
            if owner.get(suite) != shard:
                mismatch.append((run, job, suite, shard, owner.get(suite)))
            tgt = cut if verdict == "TIMEOUT" else best
            if w > tgt[suite][0]:
                tgt[suite] = (w, run, job)
        if selected == len(out):
            o = dur - sum(w for _, _, w in out)
            if o > ovh[shard][0]:
                ovh[shard] = (o, job)
    print(f"completed verdict windows: {windows}; excluded runs: {sorted(exclude) or 'none'}")
    print("shard-assignment mismatches vs head:", mismatch or "none")
    print("\nsuite | max completed window (run/job) | max TIMEOUT cutoff | limit | usage")
    for s in sorted(set(best) | set(cut)):
        lim = OLD.get(s, 1800)
        b, c = best[s], cut[s]
        use = max(b[0], c[0]) / lim * 100
        if use > 60:
            print(f"{s} | {b[0]:.3f} ({b[1]}/{b[2]}) | {c[0]:.3f} ({c[1]}/{c[2]}) | {lim} | {use:.2f}%")
    print("\nshard | changed limits | sibling maxima | max overhead (job) | envelope | headroom | max observed job time (job)")
    for sh in range(5):
        suites = [s for s, o in owner.items() if o == sh]
        lim = sum(NEW[s] for s in suites if s in NEW)
        sib = sum(max(best[s][0], cut[s][0]) for s in suites if s not in NEW)
        o = ovh[sh]
        env = lim + sib + o[0]
        print(f"{sh}/5 | {lim} | {sib:.3f} | {o[0]:.3f} ({o[1]}) | {env:.3f} | "
              f"{JOB_TIMEOUT - env:.3f} / {(JOB_TIMEOUT - env) / JOB_TIMEOUT * 100:.2f}% | "
              f"{total[sh][0]:.0f} ({total[sh][1]})")


if __name__ == "__main__":
    main(sys.argv)
