#!/usr/bin/env python3
"""Summarise a lockprobe sweep file per (rate, jitter)."""
import re, sys, collections
rows = [l for l in open(sys.argv[1]) if l.startswith("RES ")]
g = collections.defaultdict(list)
for l in rows:
    kv = dict(re.findall(r"(\w+)=([^\s\[]+)", l.split(" [")[0]))
    gaps = re.search(r"nco_gaps acq=(\d+) lock=(\d+)", l)
    surs = re.findall(r"sur@(\d+)=(\d+)/(\d+)(\(merged\))?(\(ambig\))?", l)
    bad = [s for s in surs if not s[3] and not s[4] and (s[1], s[2]) != ("0", "1")]
    amb = [s for s in surs if s[4]]
    ld, ls = map(int, kv["lock"].split("/"))
    hd, hs = map(int, kv["held"].split("/"))
    g[(kv["rate"], int(kv["jit"]))].append(dict(lead=int(kv["lead"]), lock=ld + ls,
        clr=int(kv["clr"]), held=(hd, hs), gacq=int(gaps.group(1)), glock=int(gaps.group(2)),
        badsur=len(bad), ambsur=len(amb), acq=kv["acq"]))
print("rate jit runs lock_clean min_clr clr<12 held_exact surplus_exact(non-ambig) nco_gap_runs(acq) nco_gaps(lock) ambiguous_surplus_skipped")
for k in sorted(g):
    r = g[k]
    print(k[0], k[1], len(r), sum(x["lock"] == 0 for x in r), min(x["clr"] for x in r),
          sum(x["clr"] < 12 for x in r), sum(x["held"] == (1, 0) for x in r),
          sum(x["badsur"] == 0 for x in r), sum(x["gacq"] > 0 for x in r),
          sum(x["glock"] for x in r), sum(x["ambsur"] for x in r))
    for x in r:
        if x["lock"] or x["clr"] < 12 or x["badsur"] or x["held"] != (1, 0):
            print("   exception lead=%d lock_counts=%d clr=%d held=%s badsur=%d nco_gaps_acq=%d acq=%s"
                  % (x["lead"], x["lock"], x["clr"], x["held"], x["badsur"], x["gacq"], x["acq"]))
