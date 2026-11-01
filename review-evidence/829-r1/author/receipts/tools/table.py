#!/usr/bin/env python3
"""The before-and-after table of REPORT.md, from the row.json files present plus the two rows measured before this lane."""
import json, os
R = "$MANAGEMENT/2026-09-23/829-a725b/receipts/"
ROW = {"asfound": (2373.8, 855.9), "fault3-reset-1": (2415.2, 932.0)}
rows = [
 ("f-01-pair-0-0", "final image, written 0/0"),
 ("f-02-pair-400-0", "400/0, sum 400"),
 ("f-03-pair-0-400", "0/400, sum 400"),
 ("f-04-pair-800-400", "800/400, sum 1200"),
 ("f-00-after-flash-reset-pair", "reset value, right after the flash"),
 ("f-05-pair-from-math", "pair from `f-01`'s capture, 1405/100"),
 ("f-06-true-pair-reset-value", "**true pair**, 1409/100, the reset value"),
 ("f-07-tap-comp", "**tap compensation**, 1409/581"),
 ("f-10-tap-comp-sync-a", "the same, first 5 min 20 s"),
 ("f-11-tap-comp-sync-b", "the same, next 5 min 20 s"),
 ("bench-left", "bench as left"),
]
print("| Setting | Tap | Exchanges | Arty, sd | Zero, sd | Arty - zero | Sum | PDELAY_NS mean (range) | GPTP_LAT | ASCAP | SYNC |")
print("|---|---|---:|---:|---:|---:|---:|---|---|---|---|")
print("| Uncalibrated fixed image (scratch probe build), measured before this lane | out | status only | | | | 1504 (2 x 752) | 748 to 756 | | 1 | 1 |")
print("| The same image | in | 129 | 2368.4, 33.2 | 859.0, 22.7 | 1509.4 | 1509.4 | 1620 | | 0 | 0 |")
for d, label in rows:
    r = json.load(open(R + d + "/row.json"))
    print(f"| {label} (`{d}`) | in | {r['n_arty']} | {r['arty']}, {r['arty_sd']} | {r['zero']}, {r['zero_sd']} | {r['residual']} | {r['sum']} | {r['pdelay_mean']} ({r['pdelay_min']} to {r['pdelay_max']}) | `{r['gptp_lat']}` | {'/'.join(r['ascapable'])} | {'/'.join(r['sync'])} |")
b = json.load(open(R + "f-01-pair-0-0/row.json"))
print()
print("| Row against `f-01`, same link-up | X written | Arty moved, predicted -X | Sum | PDELAY_NS moved, predicted -X/2 |")
print("|---|---:|---:|---:|---:|")
for d in ("f-02-pair-400-0", "f-03-pair-0-400", "f-04-pair-800-400", "f-05-pair-from-math", "f-06-true-pair-reset-value", "f-07-tap-comp", "f-10-tap-comp-sync-a", "f-11-tap-comp-sync-b"):
    r = json.load(open(R + d + "/row.json"))
    x = r["ingress"] + r["egress"]
    print(f"| `{d}` | {x} | {r['arty'] - b['arty']:.1f} | {r['sum']} | {r['pdelay_mean'] - b['pdelay_mean']:.1f} |")
print()
print("| Link-up | Image | Pair | Arty | Zero | Sum |")
print("|---|---|---|---:|---:|---:|")
print("| 14:05 | scratch probe | none | 2368.4 | 859.0 | 1509.4 |")
for label, img, d in (("14:24, same link-up", "scratch probe", "asfound"), ("14:25, reset", "scratch probe", "fault3-reset-1"),
                      ("15:29, flash 1", "`0a1928bd`", "m-01-pair-0-0"), ("15:34, reset", "`0a1928bd`", "m-11-reset1-pair-0-0"), ("15:35, reset", "`0a1928bd`", "m-12-reset2-pair-0-0"),
                      ("15:36, reset, measured at 16:01", "`0a1928bd`", "m-14-same-link-up-pair-0-0"), ("16:28, flash 2", "final", "f-01-pair-0-0")):
    if os.path.exists(R + d + "/row.json"):
        r = json.load(open(R + d + "/row.json")); print(f"| {label} | {img} | 0/0 | {r['arty']} | {r['zero']} | {r['sum']} |")
    else:
        print(f"| {label} | {img} | none | {ROW[d][0]} | {ROW[d][1]} | {ROW[d][0]-ROW[d][1]:.1f} |")
