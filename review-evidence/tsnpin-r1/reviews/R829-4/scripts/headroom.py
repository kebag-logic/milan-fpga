"""Recompute each receipt point's banks and tiles with the head's ctrl_memory.banks, and the bytes each region
may grow before its next granule. Usage: python3 -I headroom.py <repo> <author-r4 round4 receipts dir>"""
import glob, json, sys
from pathlib import Path
repo, rec = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "sw/litex"))
import ctrl_memory as cm
rows = []
for d in ("fixture-merge", "platform-merge", "fixture-0fb66211", "platform-0fb66211"):
    for f in sorted(glob.glob(str(rec / d / "*.size.json"))):
        s = json.load(open(f))["split"]
        out = []
        for reg in ("rom", "sram"):
            need = s[reg]["bytes"]; b = cm.banks(need)
            assert list(b) == s[reg]["banks"], (f, reg, b, s[reg]["banks"])
            out.append((reg, need, sum(b) - need))
        tiles = sum(len([x for x in cm.banks(s[r]["bytes"])]) for r in ("rom", "sram"))
        g = sum(sum(cm.banks(s[r]["bytes"])) for r in ("rom", "sram")) / 4096
        assert g == s["tiles"], (f, g, s["tiles"])
        rows.append((d + "/" + Path(f).name.replace(".size.json", ""), s["tiles"], out))
for name, t, out in rows:
    print(f"{name:34s} tiles {t:5.1f}  " + "  ".join(f"{r} need {n:7,d} spare {sp:5,d}" for r, n, sp in out))
merge = [r for r in rows if "merge" in r[0]]
low = min(((sp, n, r) for n, _, out in merge for r, _, sp in out))
lowrom = min(((sp, n) for n, _, out in merge for r, _, sp in out if r == "rom"))
print("merge: smallest spare of any region:", low, " smallest rom spare:", lowrom)
