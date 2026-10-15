#!/usr/bin/env python3
"""The primed-margin bounds each B17 cycle supports, from its summary JSON alone.

usage: b17_bound.py <dir holding c01.json .. c10.json>

Per cycle: the slip interval (poll.slips[0]); bursts are late_pdus (the reader's
list of PDUs more than 10 us late) grouped while consecutive entries are under
5 ms apart. The first burst is the one inside the slip interval: it slipped the
ring, so the primed margin was below its peak. Every burst after the slip
interval met a ring one tick (1e6 / 48000 us) further from its empty edge and
slipped nothing, so the margin was above (largest later peak - 1 tick).
The list's 10 us threshold is printed, never used as a bound.
"""
import glob
import json
import sys

TICK_US = 1e6 / 48000.0
lo_all, hi_all = [], []
for f in sorted(glob.glob(sys.argv[1] + "/c*.json")):
    d = json.load(open(f))
    if "tap" not in d:
        continue
    sl = d["poll"]["slips"][0]
    bursts = []
    for p in d["tap"]["late_pdus"]:
        if bursts and p["s"] - bursts[-1][-1]["s"] < 0.005:
            bursts[-1].append(p)
        else:
            bursts.append([p])
    peaks = [(x[0]["s"], max(y["late_us"] for y in x)) for x in bursts]
    pre = [b for b in peaks if b[0] < sl["s_lo"]]
    first = [b for b in peaks if sl["s_lo"] <= b[0] <= sl["s_hi"]]
    later = [b for b in peaks if b[0] > sl["s_hi"]]
    hi = min(b[1] for b in first)
    lo = max(b[1] for b in later) - TICK_US
    lo_all.append((lo, d["cycle"]))
    hi_all.append((hi, d["cycle"]))
    print(f"{d['cycle']}: slip {sl['s_lo']}..{sl['s_hi']} s, +{sl['dups']} dups; listed bursts before it {len(pre)}; "
          f"first burst peak {hi:.3f} us; {len(later)} later bursts, largest {lo + TICK_US:.3f} us; "
          f"margin bound {lo:.3f} < m < {hi:.3f} us")
lo, lc = max(lo_all)
hi, hc = min(hi_all)
print(f"tick {TICK_US:.6f} us; tightest lower bound {lo:.6f} us ({lc}); tightest upper bound {hi:.3f} us ({hc})")
print(f"other cycles' lower bounds {min(v for v, c in lo_all if c != lc):.3f} to "
      f"{max(v for v, c in lo_all if c != lc):.3f} us; upper bounds {min(v for v, c in hi_all if c != hc):.3f} to "
      f"{max(v for v, c in hi_all if c != hc):.3f} us")
print("the reader's late-PDU threshold (10 us) is a reporting threshold and bounds nothing")
