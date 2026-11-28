"""The 100 Mb/s envelope of the Arty 4x4/1if image, by Milan v1.2 4.3.3.2 Table 4.4's recipe, against 802.1Q 34.3.1's
75 % class-A limit, each direction separately (full duplex)."""
import json
LINK = 100_000  # kb/s
LIMIT = 75 * LINK // 100
def aaf_kbps(ch, rate):
    spf = rate // 8000
    mfs = 4 * spf * ch + 24 + 1                 # Table 4.4: MaxFrameSize, PCM32
    f = max(mfs + 22, 68); w = f + 20           # steps 1-3
    return w * 8000 * 8 / 1000, mfs
CRF = (max(28 + 1 + 22, 68) + 20) * 8000 * 8 / 1000   # 5632 kb/s
rows = []
for rate in (48000, 96000, 192000):
    for ch in (1, 2, 4, 6, 8):
        kb, mfs = aaf_kbps(ch, rate)
        four = 4 * kb + CRF
        rows.append(dict(rate=rate, ch=ch, max_frame=mfs, kbps=kb, four_plus_crf=four, fits_four=four <= LIMIT,
                         pct_of_limit=round(100 * four / LIMIT, 1)))
# gPTP egress (802.1AS-2020; Milan log intervals: sync -3, announce 0, pdelay 0): frame octets on the line
line = lambda n: 8 + max(n, 60) + 4 + 12
gptp = (8 * (line(58) + line(90)) + 1 * (line(90) + 3 * line(68))) * 8 / 1000
egress = 4 * aaf_kbps(2, 48000)[0] + CRF
ingress = 4 * aaf_kbps(8, 48000)[0] + CRF
out = dict(link_kbps=LINK, class_a_limit_kbps=LIMIT, crf_kbps=CRF, gptp_egress_kbps=gptp,
           egress_reserved_kbps=egress, egress_free_for_best_effort_kbps=LINK - egress - gptp,
           ingress_worst_reserved_kbps=ingress, formats=rows)
print(json.dumps(out, indent=1))
