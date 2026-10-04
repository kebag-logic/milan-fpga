#!/usr/bin/env python3
"""R456-3: re-measure the walk and the band margins from every leg log under
PACKET/receipts (probes and suites). Usage: r3_walks.py PACKET

For every window line the head prints, the nearest-pop range (dmin..dmax),
the printed walk, and whether the walk equals dmax - dmin (or, on a wrap line,
the first-pop-after range). For every graded law line, how far its first-event
delays sit inside the band (lo = 8 T, hi = 9 T + 1 cycle). Logs of builds whose
window is not the head's (the w4/w0 guard ablations, the crfw1104 widening)
are reported apart, because they grade at a different W. Then: the largest
walk per log, per window kind ([LAW] settled and held, [LAW] not held, CRF),
and overall for the sound design at W = 9."""
import re
import sys
from pathlib import Path

P = Path(sys.argv[1]).resolve()
T = 100e6 / 48000.0
LO, HI = 8 * T, 9 * T + 1
OFF = re.compile(r"\[i\]\s+(T30 [^:]+): over (\d+) steady PDU ends the first pop after the end "
                 r"is taken ([+-]\d+)\.\.([+-]\d+) cycles from it and the pop nearest the "
                 r"boundary ([+-]\d+)\.\.([+-]\d+) \(walk (\d+)\); the least clearance is "
                 r"(\d+) cycles.*?margin (-?\d+)(.*)")
LAW = re.compile(r"\[i\]\s+(T30 [^:]+): (\d+) PDUs, fill at the PDU end (\d+)\.\.(\d+), "
                 r"first-event delay from it (\d+)\.\.(\d+) cycles")
NOT_HEAD_W = ("w4", "w0", "spm1w0", "spp1w0", "crfw1104")
out: list[str] = []
w = out.append
agg = {"LAW held": 0, "LAW not held": 0, "CRF": 0}
band_min = None
mismatch = 0
wraps = 0
for log in sorted(list((P / "receipts/probes").glob("*.log")) +
                  list((P / "receipts/suites").glob("suite-*.log"))):
    text = log.read_text(errors="replace")
    name = log.name
    other_w = any(f"-{k}-" in name for k in NOT_HEAD_W)
    held_fail = {m[1] for m in re.finditer(r"\[FAIL\] (T30 INTERNAL LAW \+\d+): the aligner held", text)}
    lmax = -1
    for m in OFF.finditer(text):
        tag, nmin, nmax, dmin, dmax, walk = m[1], int(m[3]), int(m[4]), int(m[5]), int(m[6]), int(m[7])
        wrap = "changes side" in m[10]
        wraps += wrap
        expect = (nmax - nmin) if wrap else (dmax - dmin)
        if walk != expect:
            mismatch += 1
            w(f"  MISMATCH {name}: {tag} walk {walk} vs range {expect}")
        lmax = max(lmax, walk)
        if other_w:
            continue
        kind = "CRF" if "CRF" in tag else ("LAW not held" if tag in held_fail else "LAW held")
        agg[kind] = max(agg[kind], walk)
    if not other_w and "base-full" not in name:
        for m in LAW.finditer(text):
            lo_in, hi_in = int(m[5]) - LO, HI - int(m[6])
            if "spm1" in name or "spp1" in name:
                continue
            b = min(lo_in, hi_in)
            if band_min is None or b < band_min[0]:
                band_min = (b, name, m[1], int(m[5]), int(m[6]))
    w(f"{name:34} largest walk {lmax if lmax >= 0 else '-'}{'  (W != 9 build)' if other_w else ''}")
w("")
w(f"walk printed == its own range on every line: {mismatch == 0} ({mismatch} mismatches; "
  f"{wraps} wrap lines)")
w(f"largest walk, sound-design W = 9 logs: [LAW] settled and held {agg['LAW held']}, "
  f"[LAW] whose settled hold failed {agg['LAW not held']}, CRF {agg['CRF']}")
if band_min:
    b, name, tag, dmin, dmax = band_min
    w(f"least band margin over graded sound-design windows: {b:.2f} cycles "
      f"({name}, {tag}, delays {dmin}..{dmax}; lo {LO:.2f}, hi {HI:.2f})")
print("\n".join(out))
