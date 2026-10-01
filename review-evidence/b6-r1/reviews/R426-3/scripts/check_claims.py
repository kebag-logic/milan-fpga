#!/usr/bin/env python3
"""R426-3: re-derive the round-3 page claims from the published grades.

Usage: check_claims.py <archive-root>   (the review-evidence/b6-r1 directory)
Reads author/summary/<case>/grade.json (skip_clusters) only. Prints each claim,
the derived value and OK/MISMATCH; RESULT PASS when every claim holds.
"""
import json, sys, pathlib, collections

root = pathlib.Path(sys.argv[1]) / "author/summary"
cases = ["a0", "a1", "a2", "bint", "bcrf"]
G = {c: json.loads((root / c / "grade.json").read_text()) for c in cases}
ok_all = True


def claim(text, got, want):
    global ok_all
    ok = got == want
    ok_all &= ok
    print(f"{'OK      ' if ok else 'MISMATCH'} {text}: got {got!r}, page {want!r}")


s48 = lambda n: n > 0 and (n - 12) % 48 == 0
for c in cases:
    cl = [k for k in G[c]["skip_clusters"] if k["capture_path"]]
    print(f"{c}: {len(cl)} capture-path clusters, basis "
          f"{dict(collections.Counter(k['basis'] for k in cl))}")

# F2(b): the gap-only (unmeasurable rise) clusters per case
gap_only = {c: [k for k in G[c]["skip_clusters"] if k["capture_path"] and k["read_rise_ms"] is None]
            for c in cases}
claim("gap-only clusters (rise unmeasurable) A0/A1/A2/BINT/BCRF",
      [len(gap_only[c]) for c in cases], [1, 2, 5, 3, 0])
claim("every skip in those eleven is 48n+12",
      all(s48(s) for c in cases for k in gap_only[c] for s in k["steps"]), True)

# F2(b): A2 clusters with a measured rise that does not match (1 ms + 2 %)
def matches(k):
    return k["read_rise_ms"] is not None and abs(k["read_rise_ms"] - k["lost_ms"]) <= 1 + 0.02 * k["lost_ms"]
nm = {c: [k for k in G[c]["skip_clusters"] if k["capture_path"] and k["read_rise_ms"] is not None
          and not matches(k)] for c in cases}
claim("measured non-matching clusters A0/A1/A2/BINT/BCRF",
      [len(nm[c]) for c in cases], [0, 0, 2, 0, 0])
claim("A2 non-matching cluster ids", sorted(k["cluster"] for k in nm["a2"]), [17, 56])
claim("A2 non-matching (rise ms, lost frames)",
      sorted((round(k["read_rise_ms"], 1), k["lost_frames"]) for k in nm["a2"]),
      sorted([(154.5, 60), (-155.8, 1020)]))
claim("A2 non-matching every step 48n+12 and basis",
      [(all(s48(s) for s in k["steps"]), k["basis"], k["recent_read_gap_ms"] >= 11) for k in nm["a2"]],
      [(True, nm["a2"][0]["basis"], True)] * 2)
print("   (basis of the two:", [k["basis"] for k in nm["a2"]], ")")
claim("all other capture-path clusters match within 1 ms + 2 %",
      all(matches(k) for c in cases for k in G[c]["skip_clusters"] if k["capture_path"]
          and k["read_rise_ms"] is not None and k not in nm[c]), True)

# F2(a): A1/B CRF clusters under 98 frames
small = [(c, k) for c in ("a1", "bcrf") for k in G[c]["skip_clusters"]
         if k["capture_path"] and abs(k["net_step"]) < 98]
claim("A1+B CRF clusters under 98 frames", len(small), 7)
claim("each is one 60-frame skip", all(k["steps"] == [60] for _, k in small), True)
claim("min read gap of the seven >= 14.9 ms",
      min(k["recent_read_gap_ms"] for _, k in small) >= 14.9, True)
meas = [(c, k) for c, k in small if k["read_rise_ms"] is not None]
claim("number with a measured rise", len(meas), 6)
claim("measured rises within 0.99..1.00 ms",
      all(0.985 <= k["read_rise_ms"] <= 1.005 for _, k in meas), True)
unm = [(c, k["cluster"], k["recent_read_gap_ms"], k["basis"]) for c, k in small if k["read_rise_ms"] is None]
claim("the unmeasurable one is A1 cluster 9", [(c, n) for c, n, _, _ in unm], [("a1", 9)])
print("   (its read gap ms and basis:", [(round(g, 3), b) for _, _, g, b in unm], ")")
claim("A1 cluster 9 is among A1's gap-only clusters",
      9 in [k["cluster"] for k in gap_only["a1"]], True)
claim("smallest A1/B CRF capture-path loss (frames)",
      min(k["lost_frames"] for c in ("a1", "bcrf") for k in G[c]["skip_clusters"] if k["capture_path"]), 60)

# S1 / path 6: member steps of A1 and B CRF clusters
odd = [(c, k["cluster"], s, len(k["steps"])) for c in ("a1", "bcrf") for k in G[c]["skip_clusters"]
       if k["capture_path"] for s in k["steps"] if not s48(s)]
print("   A1/B CRF member steps not 48n+12 (case, cluster, step, steps-in-cluster):", odd)
claim("non-48n+12 members are stale-replay edges (+-23,880/+-24,000) or the lone 18,626",
      all(abs(s) in (23880, 24000) or (s == 18626 and n == 1) for _, _, s, n in odd), True)
big = [k for k in G["a1"]["skip_clusters"] if 18626 in k["steps"]]
claim("A1 18,626-frame loss: lost ms and the 1 ms + 2 % band (about 249 ms)",
      [round(1 + 0.02 * k["lost_ms"]) for k in big], [249])
print("RESULT", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
