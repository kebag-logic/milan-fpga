"""Re-derive the round-3 attribution figures from the published hierarchy reports.
Usage: python3 -I derive_figures.py <evidence-dir> <clone>
Prints each figure the delta cites and whether it matches."""
import json, subprocess, sys
from pathlib import Path
ev, clone = Path(sys.argv[1]), sys.argv[2]
def rows(name):
    out = []
    for line in (ev / name).read_text().splitlines():
        c = line.split("|")
        if len(c) > 9 and c[1].strip() and c[1].strip() != "Instance":
            out.append((c[1].strip(), (int(c[3]), int(c[7]))))
    return out
def get(r, inst, nth=0):
    hits = [v for k, v in r if k == inst]
    return hits[nth]
R = {d: rows(f"author-r2_receipts_area_runs_{d}_baseline_hierarchy.rpt") for d in ("eppo", "aslh", "eto")}
O = {d: rows(f"author-r2_receipts_area_runs_{d}_baseline_hierarchy.rpt") for d in ("ooc-1x1", "ooc-8x8")}
bad = 0
def chk(label, got, want):
    global bad; ok = got == want; bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} {label}: {got} (text {want})")
for d, r in R.items():
    tot = get(r, "alinx_ax7101"); dp = get(r, "milan_datapath"); w = get(r, "pp_shadow")
    own = get(r, "(pp_shadow)"); kids = [get(r, n) for n in ("ctl_fifo", "u_nvm", "u_pp")]
    al = [v for k, v in r if k == "aligner"][1]
    chk(f"{d} top FF", tot[1], {"eppo": 54850, "aslh": 54847, "eto": 54847}[d])
    chk(f"{d} milan_datapath FF", dp[1], 43435)
    chk(f"{d} wrapper FF", w[1], 20038)
    chk(f"{d} write aligner FF", al[1], 146 if d == "eppo" else 143)
    chk(f"{d} own-cell LUT/FF", own, (18, 332))
    chk(f"{d} remainder LUT/FF", (w[0] - sum(k[0] for k in kids), w[1] - sum(k[1] for k in kids)), ({"eppo": 1}.get(d, 0), 332))
for d, r in O.items():
    w = get(r, "KL_pp_shadow"); own = get(r, "(KL_pp_shadow)"); kids = [get(r, n) for n in ("ctl_fifo", "u_nvm", "u_pp")]
    chk(f"{d} own-cell LUT/FF", own, {"ooc-1x1": (18, 340), "ooc-8x8": (17, 341)}[d])
    chk(f"{d} remainder LUT/FF", (w[0] - sum(k[0] for k in kids), w[1] - sum(k[1] for k in kids)), {"ooc-1x1": (-5, 340), "ooc-8x8": (-6, 341)}[d])
def rec(rev):
    return json.loads(subprocess.check_output(["git", "-C", clone, "show", f"{rev}:syn/ooc/pp_resource_baseline.json"]))
a, b = rec("ac0a01e3"), rec("a853461dd57f8e493ca079e0faa1f07229c3cb16")
def sc(x, ep, s): return x["endpoints"][ep]["record"]["scopes"][s]
for ep, want in (("route-1x1", (8, 9)), ("ooc-1x1", (7, 9)), ("ooc-8x8", (6, 9))):
    def rem(x):
        w = sc(x, ep, "wrapper"); k = [sc(x, ep, n) for n in ("ctl_fifo", "u_nvm", "u_pp")]
        return w["LUT"] - sum(i["LUT"] for i in k), w["FF"] - sum(i["FF"] for i in k)
    ra, rb = rem(a), rem(b)
    chk(f"{ep} remainder change LUT/FF (record 15 -> 16)", (rb[0] - ra[0], rb[1] - ra[1]), want)
    chk(f"{ep} wrapper FF change", sc(b, ep, "wrapper")["FF"] - sc(a, ep, "wrapper")["FF"], 10)
chk("record 15 route FF", a["endpoints"]["route-1x1"]["record"]["figures"]["FF"], 54837)
print(f"{'ALL OK' if not bad else 'FAIL'}: {bad} difference(s)")
sys.exit(1 if bad else 0)
