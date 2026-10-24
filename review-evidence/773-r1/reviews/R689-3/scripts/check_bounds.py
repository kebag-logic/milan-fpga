"""Independent exact-arithmetic recomputation of every figure the #773 delta adds to
docs/design/MEDIA_CLOCK_FOLLOWING.md and docs/reference/MILAN_COMPLIANCE_MATRIX.md, plus a check of the
page's capture_coherence [HOLD] sentence against a capture_coherence dp-leg log or excerpt: the maxima and run
counts the page states are rebuilt from the log, and the earlier "in every 2 ms run" claim must be absent.

usage: python3 -I check_bounds.py <repo-checkout> <capture_coherence log or excerpt>
Inputs are the shipping-shape terms elaborated in the round-1 probes (marker latency, capture age, walk,
packetizer, CRF path) and the line-rate frame sizes; every derived figure is computed here, then each is
required to appear verbatim in the page text. Exit 0 only if every figure checks and the page is found.
"""
from fractions import Fraction as F
from math import ceil, floor
import pathlib, re, sys

repo, cclog = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
page = (repo / "docs/design/MEDIA_CLOCK_FOLLOWING.md").read_text()
matrix = (repo / "docs/reference/MILAN_COMPLIANCE_MATRIX.md").read_text()
flat = re.sub(r"\s+", " ", page)
fails = 0


def chk(name, got, want, text=None):
    global fails
    ok = got == want
    where = ""
    if text is not None:
        hit = text in flat or text in matrix
        ok = ok and hit
        where = f" [page text {'found' if hit else 'MISSING'}: {text!r}]"
    print(f"{'PASS' if ok else 'FAIL'} {name}: computed {got} expected {want}{where}")
    fails += not ok


def ns(x):  # nearest ns, as the page states its figures
    return int(floor(F(x) + F(1, 2)))


FS, CLK = 48_000, 50_000_000
PS = F(10**9, FS)                      # 20,833.33 ns
CYC = F(10**9, CLK)                    # 20 ns
LEAD = ceil(8 * PS)                    # stamp lead, rounded up once
OFS2, OFS125 = 2_000_000, 125_000
shape = {  # marker latency ns, walk to talker 0 last pair (cycles), walk to last talker's last pair, pipe t0, pipe last
    "1x1": dict(mlat=20_964, walk0=4 + 4 + 26 * 3, walk_last=86, pipe0=57, pipe_last=57, K=2, crf=21_164),
    "8x8": dict(mlat=5_308, walk0=4 + 1 + 26 * 3, walk_last=811, pipe0=57, pipe_last=60, K=1, crf=5_508),
}
ROWS = 128
chk("lead 8 Ps rounded up", LEAD, 166_667, "166,667 ns")

for s, d in shape.items():
    span = d["mlat"] - floor(PS)       # TLK_SPAN_NS_C: marker latency less floor(Ps)
    # queue range (the page's supported-range table)
    lo = ns(d["K"] * PS - d["mlat"] + PS / 2)
    hi = ns((d["K"] + ROWS - F(3, 2)) * PS - d["mlat"])
    chk(f"{s} queue lower", lo, {"1x1": 31_119, "8x8": 25_942}[s])
    chk(f"{s} queue upper", hi, {"1x1": 2_656_119, "8x8": 2_650_942}[s])
    # grid-live earliest hand-over after the frame's instant: span end + span term + age 0 + walk + pipe (talker 0)
    gl = 6 * PS + span + (d["walk0"] + d["pipe0"]) * CYC
    gl = ns(gl)
    chk(f"{s} grid-live earliest hand-over", gl, {"1x1": 127_991, "8x8": 112_275}[s])
    glmax = OFS2 + LEAD - gl
    chk(f"{s} grid-live arrival lead at 2 ms", glmax, {"1x1": 2_038_676, "8x8": 2_054_392}[s])
    gl_last = glmax + ns(5 * PS)
    chk(f"{s} grid-live last event after arrival", gl_last, {"1x1": 2_142_843, "8x8": 2_158_559}[s])
    chk(f"{s} grid-live margin (0.1 us)", round((hi - gl_last) / 100) / 10, {"1x1": 513.3, "8x8": 492.4}[s])

# start-up PDU: live-PHC base at its first pair; five tick spacings (integer cycles, at least floor(5 Ps / cyc)),
# the walk from its first to its last pair (3 pair steps of 26 cycles), the packetizer for talker 0
tick5 = floor(5 * PS / CYC)
chk("five tick spacings, cycles at least", tick5, 5_208, "5,208 cycles at least")
walk_on = 26 * 3
chk("walk on to the last pair", walk_on, 78, "(78 cycles)")
su_cyc = tick5 + walk_on + 57
chk("start-up hand-over cycles", su_cyc, 5_343, "5,343 cycles")
su_ns = su_cyc * CYC
chk("start-up hand-over ns", su_ns, 106_860, "106,860 ns")
su2 = OFS2 + LEAD - su_ns
su125 = OFS125 + LEAD - su_ns
chk("start-up arrival lead at 2 ms", su2, 2_059_807, "2,059,807 ns before its timestamp")
chk("start-up arrival lead at 125 us", su125, 184_807, "(184,807 ns at 125 us)")
chk("start-up lead with one more cycle (the measured 2,059,787)", OFS2 + LEAD - (su_cyc + 1) * CYC, 2_059_787)
su_last = su2 + ns(5 * PS)
chk("start-up last event after arrival", su_last, 2_163_974, "2,163,974 ns after arrival")
for s, want in (("1x1", 492.1), ("8x8", 487.0)):
    hi = {"1x1": 2_656_119, "8x8": 2_650_942}[s]
    chk(f"{s} start-up margin (0.1 us)", round((hi - su_last) / 100) / 10, want)
chk("inside 2.126 ms (Milan v1.2 4.4.2.1)", su2 < 2_126_000 and 2_054_392 < 2_126_000, True)
# Equation (1) lower bound: lead < earliest hand-over + TUmax (125 us)
ceil_lead = su_ns + 125_000
chk("Eq.(1) lead ceiling >= stated 231.8 us and lead below it", (ceil_lead >= 231_800, LEAD < 231_800), (True, True),
    "any lead up to 231.8 us holds")
chk("Eq.(1) lead ceiling (exact, ns)", ceil_lead, 231_860)
chk("drift: 5 Ps x 1000 ppm", ns(5 * PS * F(1, 1000)), 104, "(104 ns at 1,000 ppm)")
chk("drift: 5 Ps", ns(5 * PS), 104_167, "104,167 d ns")

# supported range for this device's talker: lead = offset + LEAD - transit, first event in [lo, hi]
for s in shape:
    lo = {"1x1": 31_119, "8x8": 25_942}[s]; hi = {"1x1": 2_656_119, "8x8": 2_650_942}[s]
    chk(f"{s} transit bound at 2 ms", OFS2 + LEAD - lo, {"1x1": 2_135_548, "8x8": 2_140_725}[s])
    chk(f"{s} first-event offset bound", hi - LEAD, {"1x1": 2_489_452, "8x8": 2_484_275}[s])
    chk(f"{s} whole-PDU offset bound", hi - LEAD - ns(5 * PS), {"1x1": 2_385_285, "8x8": 2_380_108}[s])
for t in ("2,135,548 ns (1x1) or 2,140,725 ns (8x8)", "2,489,452 ns (1x1) or 2,484,275 ns (8x8)",
          "2,385,285 or 2,380,108 ns"):
    chk("range text", True, True, t)

# MAC level at 1 Gb/s: max tagged frame 1522 + preamble/SFD 8 + IFG 12 octets
BIT = 1  # ns per bit at 1 Gb/s
maxf = (1522 + 8 + 12) * 8 * BIT
chk("max tagged frame on the wire", maxf, 12_336, "12,336 ns")
chk("max frame at 100 Mb/s", maxf * 10, 123_360, "123,360 ns")
chk("gasket 512 cycles", 512 * CYC, 10_240, "10.24 us")
crf_w = (64 + 8 + 12) * 8          # CRF PDU: one timestamp, a minimum 64-octet frame
aaf_w = (14 + 4 + 24 + 8 * 6 * 4 + 4 + 8 + 12) * 8  # 8 ch x 6 samples x 32 bit
spare = {"aaf1": 17_816, "aaf8": 18_912, "crf1": 20_503, "crf8": 15_326}
for k, want in (("aaf1", 5_480), ("aaf8", 6_576), ("crf1", 8_167), ("crf8", 2_990)):
    chk(f"one frame ahead at the MAC, {k} left", spare[k] - maxf, want)
chk("one-frame-ahead text", True, True, "5,480 ns (1x1) or 6,576 ns (8x8) for an AAF PDU, and 8,167 or 2,990 ns for a CRF PDU")
# store-and-forward: frame through the arbiters first (190 beats), then the other output's PDU, then this PDU
beat = 20
aaf_shift = 190 * beat + maxf + crf_w - 30 * beat   # vs uncontended egress at its own last beat
crf_shift = 190 * beat + maxf + aaf_w - 8 * beat
chk("AAF egress shift", aaf_shift, 16_208, "16,208 ns (AAF)")
chk("CRF egress shift", crf_shift, 18_040, "18,040 ns (CRF)")
chk("AAF left 1x1/8x8", (spare["aaf1"] - aaf_shift, spare["aaf8"] - aaf_shift), (1_608, 2_704), "1,608 or 2,704 ns for AAF")
chk("CRF 1x1 left", spare["crf1"] - crf_shift, 2_463, "2,463 ns")
chk("CRF 8x8 late", crf_shift - spare["crf8"], 2_714, "up to 2,714 ns after its timestamp less the applied offset")
chk("CRF 8x8 corner named as transit after Equation (1)'s TT", True, True,
    "That is after the hand-over, which is Equation (1)'s TT, so it is transit that the stream's latency budget carries.")

# the measured [HOLD] maxima against the stated bound and against "in every 2 ms run"
txt = cclog.read_text(errors="replace")
runs = re.findall(r"\[(DP-[^\]]+)\] \[WIRE\] offset (\d+) ns:.*?\[HOLD\] avtp_timestamp - hand-over max (\d+) ns", txt)
two = [(r, int(h)) for r, o, h in runs if o == "2000000"]
q = [(r, int(h)) for r, o, h in runs if o == "125000"]
chk("2 ms runs found", len(two), 23)
chk("every 2 ms [HOLD] <= 2,059,807", all(h <= 2_059_807 for _, h in two), True)
chk("every 125 us [HOLD] <= 184,807", all(h <= 184_807 for _, h in q), True)
at = [r for r, h in two if h == 2_059_807]
print(f"INFO 2 ms runs whose [HOLD] max equals 2,059,807: {len(at)} of {len(two)}; others: "
      f"{sorted({h for _, h in two if h != 2_059_807})}")
old = "measures that `[HOLD]` maximum in every 2 ms run"
print(f"{'FAIL' if old in flat else 'PASS'} earlier claim {old!r} absent from the page (present: {old in flat})")
fails += old in flat
hs = sorted({h for _, h in two}, reverse=True)
chk("2 ms [HOLD] maxima take exactly two values", len(hs), 2)
top, rest = hs[0], hs[-1]
n_top, n_rest = sum(h == top for _, h in two), sum(h == rest for _, h in two)
chk("largest 2 ms [HOLD] maximum is the derived bound", top, su2)
chk("the lower value is one cycle under the bound", top - rest, int(CYC))
want = (f"reaches that bound: its largest 2 ms `[HOLD]` maximum is {top:,} ns, in {n_top} of its {len(two)} runs; "
        f"the other {n_rest} reach {rest:,} ns, where the five tick spacings take one cycle more.")
chk(f"page sentence from the log ({n_top} and {n_rest} of {len(two)})", True, True, want)
print(f"{'ALL PASS' if not fails else f'{fails} FAIL'}")
sys.exit(1 if fails else 0)
