#!/usr/bin/env python3
"""Check the B6 page's round-3 statements against the published grades (read-only).

usage: round3_checks.py <evidence_repo> <archive_commit>

Reads, with `git show` only, review-evidence/b6-r1/author/summary/<case>/grade.json and
events.csv at <archive_commit>. Prints the facts behind:
  item 4  A1's and B CRF's clusters under 98 frames: which have a measured rise, which not;
  item 6  every member step of A1's and B CRF's capture-path clusters, and the rise tolerance
          at A1's 12.4 s loss; no one-frame event in any cluster;
  capture-path bullet  per case, the clusters with no measurable rise (basis "read gap") and
          their skip sizes, and the clusters with a measured, non-matching rise.
Exit 0 only when every printed statement holds.
"""
import csv
import io
import json
import subprocess
import sys

repo, commit = sys.argv[1:3]
base = "review-evidence/b6-r1/author/summary"
CASES = ["a0", "a1", "a2", "bint", "bcrf"]
ok = True


def show(path):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], check=True,
                          capture_output=True).stdout.decode()


def check(cond, text):
    global ok
    ok &= bool(cond)
    print(("  HOLDS  " if cond else "  FAILS  ") + text)


g = {c: json.loads(show(f"{base}/{c}/grade.json")) for c in CASES}
ev = {c: list(csv.DictReader(io.StringIO(show(f"{base}/{c}/events.csv")))) for c in CASES}
cap = {c: [s for s in g[c]["skip_clusters"] if s["capture_path"]] for c in CASES}
print(f"archive {commit}")

print("item 4: A1 and B CRF capture-path clusters under 98 frames")
small = [(c, s) for c in ("a1", "bcrf") for s in cap[c] if s["lost_frames"] < 98]
for c, s in small:
    print(f"    {c} cluster {s['cluster']}: steps {s['steps']}, rise {s['read_rise_ms']} ms, "
          f"read gap {s['recent_read_gap_ms']} ms, basis {s['basis']!r}")
rised = [s for _, s in small if s["read_rise_ms"] is not None]
norise = [(c, s) for c, s in small if s["read_rise_ms"] is None]
check(len(small) == 7 and all(s["steps"] == [60] for _, s in small), "seven clusters, each one 60-frame skip")
check(min(s["recent_read_gap_ms"] for _, s in small) >= 14.9, "every read gap 14.9 ms or more")
check(len(rised) == 6 and all(0.99 <= s["read_rise_ms"] <= 1.0049 for s in rised),
      f"six have a measured rise, {min(s['read_rise_ms'] for s in rised)} to "
      f"{max(s['read_rise_ms'] for s in rised)} ms (0.99 to 1.00 ms)")
check(len(norise) == 1 and norise[0][0] == "a1" and norise[0][1]["cluster"] == 9
      and norise[0][1]["basis"] == "read gap" and round(norise[0][1]["recent_read_gap_ms"]) == 33,
      "the seventh is A1 cluster 9: no measurable rise, basis 'read gap' (gap-only), after a 33 ms read gap")
check(sorted(s["cluster"] for s in cap["a1"] if s["basis"] == "read gap") == [2, 9],
      "A1's two gap-only clusters are 2 and 9, so cluster 9 is one of item 5's two")

print("item 6: member steps of every capture-path cluster in A1 and B CRF")
for c in ("a1", "bcrf"):
    odd = []
    for s in cap[c]:
        for st in s["steps"]:
            if st > 0 and st % 48 == 12:
                continue
            odd.append((s["cluster"], st, len(s["steps"])))
    print(f"    {c}: {sum(len(s['steps']) for s in cap[c])} member steps; not 48 n + 12: {odd}")
a1_odd = [(cl, st, n) for s in cap["a1"] for cl, st, n in
          [(s["cluster"], st, len(s["steps"])) for st in s["steps"]] if not (st > 0 and st % 48 == 12)]
b_odd = [(s["cluster"], st) for s in cap["bcrf"] for st in s["steps"] if not (st > 0 and st % 48 == 12)]
check(sorted(st for _, st, _ in a1_odd) == [-23880, 18626, 23880]
      and [n for _, st, n in a1_odd if st == 18626] == [1],
      "A1: the only other steps are the 23,880 replay edge and its exact -23,880 return, and the "
      "18,626 of the 12.4 s loss, the only step in its cluster")
check(sorted(st for _, st in b_odd) == [-24000, -24000], "B CRF: the only other steps are two exact -24,000 replay steps")
big = [s for s in cap["a1"] if s["whole_loops_added"] == 12][0]
tol = 1.0 + 0.02 * big["lost_ms"]
check(round(tol) == 249, f"A1's 12.4 s loss: {big['lost_ms']} ms lost, tolerance 1 ms + 2 % = {tol:.2f} ms (about 249 ms)")
for c in CASES:
    joined = [e for e in ev[c] if abs(int(e["step"])) == 1 and e["cluster"] not in ("", "None")]
    check(not joined, f"{c}: no one-frame event carries a cluster ({sum(abs(int(e['step'])) == 1 for e in ev[c])} one-frame events)")

print("capture-path bullet: clusters without a matching measured rise")
want_gap = {"a0": 1, "a1": 2, "a2": 5, "bint": 3, "bcrf": 0}
n_gap = 0
for c in CASES:
    gap_only = [s for s in cap[c] if s["basis"] == "read gap"]
    n_gap += len(gap_only)
    all12 = all(st % 48 == 12 for s in gap_only for st in s["steps"])
    check(len(gap_only) == want_gap[c] and all(s["read_rise_ms"] is None for s in gap_only) and all12,
          f"{c}: {len(gap_only)} gap-only clusters {[s['cluster'] for s in gap_only]}, rise unmeasurable, "
          f"every skip 48 n + 12")
check(n_gap == 11, f"{n_gap} gap-only clusters in all")
sized = [(c, s) for c in CASES for s in cap[c] if s["basis"] == "read gap and 48 n + 12 size"]
for c, s in sized:
    print(f"    {c} cluster {s['cluster']}: rise {s['read_rise_ms']} ms, loss {s['lost_frames']} frames "
          f"({s['lost_ms']} ms), read gap {s['recent_read_gap_ms']} ms")
check([(c, s["cluster"]) for c, s in sized] == [("a2", 17), ("a2", 56)],
      "only A2 clusters 17 and 56 passed on the read gap and size rule")
s17 = [s for c, s in sized if s["cluster"] == 17][0]
s56 = [s for c, s in sized if s["cluster"] == 56][0]
check(round(s17["read_rise_ms"], 1) == 154.5 and s17["lost_frames"] == 60, "cluster 17: 154.5 ms against 60 frames")
check(round(s56["read_rise_ms"], 1) == -155.8 and s56["lost_frames"] == 1020,
      "cluster 56: -155.8 ms against 1,020 frames")
longest = g["a2"]["capture_reads"]["read_gap_ms_max"]
prev = [s for s in cap["a2"] if s["cluster"] == 55][0]
check(s56["recent_read_gap_ms"] == longest and round(longest / 1000, 1) == 13.3
      and prev["recent_read_gap_ms"] == longest,
      f"cluster 56 follows cluster 55 and its look-back holds the {longest} ms (13.3 s) stall")

print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
