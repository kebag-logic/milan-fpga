#!/usr/bin/env python3
"""Re-derive the round 3 attribution figures from published artifacts (#854).

Arguments: <runs-dir> <record15.json> <record16.json>
  runs-dir holds <run>/baseline_hierarchy.rpt for eppo, aslh, eto, ooc-1x1, ooc-8x8
  (record 16's runs); the two JSON files are syn/ooc/pp_resource_baseline.json at
  dev ac0a01e3 (record 15) and at the lane head (record 16).
Prints: the route FF totals per directive; rows whose FF differ between the head's
EPPO and ASLH routes (depth <= 4); the wrapper's total, own-cell row, children sum
and total-minus-children in every run; the gate records' wrapper-scope deltas.
"""

import hashlib
import json
import sys
from pathlib import Path

COLS = ["lut", "logic", "lutram", "srl", "ff", "ramb36", "ramb18", "dsp"]


def parse(path: Path):
    rows = []
    for line in path.read_text().splitlines():
        if not line.startswith("| ") or "Instance" in line:
            continue
        cells = line.split("|")[1:-1]
        if len(cells) < 2 + len(COLS):
            continue
        name_cell = cells[0]
        depth = (len(name_cell) - len(name_cell.lstrip(" ")) - 1) // 2
        try:
            nums = [int(c.strip()) for c in cells[2:2 + len(COLS)]]
        except ValueError:
            continue
        rows.append((depth, name_cell.strip(), dict(zip(COLS, nums))))
    paths, stack = [], []
    for depth, name, figs in rows:
        stack = stack[:depth] + [name]
        paths.append(("/".join(stack), depth, figs))
    return paths


def wrapper(paths, wrapper_path):
    table = {p: (d, f) for p, d, f in paths}
    total = table[wrapper_path][1]
    depth = table[wrapper_path][0]
    own = None
    kids = []
    for p, d, f in paths:
        if p.startswith(wrapper_path + "/") and d == depth + 1:
            if p.rsplit("/", 1)[1].startswith("("):
                own = f
            else:
                kids.append((p.rsplit("/", 1)[1], f))
    ksum = {c: sum(f[c] for _, f in kids) for c in ("lut", "ff")}
    return total, own, kids, ksum


def main() -> int:
    runs, r15, r16 = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    reports = {name: runs / name / "baseline_hierarchy.rpt"
               for name in ("eppo", "aslh", "eto", "ooc-1x1", "ooc-8x8")}
    for name, path in reports.items():
        data = path.read_bytes()
        print(f"input {name}: sha256 {hashlib.sha256(data).hexdigest()} bytes {len(data)}")
    for path in (r15, r16):
        data = path.read_bytes()
        print(f"input {path.name}: sha256 {hashlib.sha256(data).hexdigest()} bytes {len(data)}")
    parsed = {n: parse(p) for n, p in reports.items()}

    print("\n# route totals (LUT, FF) and milan_datapath FF, record 16, by directive")
    for n in ("eppo", "aslh", "eto"):
        t = {p: f for p, _, f in parsed[n]}
        print(f"  {n}: top ({t['alinx_ax7101']['lut']}, {t['alinx_ax7101']['ff']})"
              f"  milan_datapath FF {t['alinx_ax7101/milan_datapath']['ff']}"
              f"  wrapper FF {t['alinx_ax7101/milan_datapath/pp_shadow']['ff']}")

    print("\n# rows whose FF differ, record 16 EPPO minus record 16 ASLH, depth <= 4")
    e = {p: f for p, d, f in parsed["eppo"] if d <= 4}
    a = {p: f for p, d, f in parsed["aslh"] if d <= 4}
    for p in e:
        if p in a and e[p]["ff"] != a[p]["ff"]:
            print(f"  {p}: FF {e[p]['ff'] - a[p]['ff']:+d}  eppo (LUT {e[p]['lut']}, FF {e[p]['ff']})"
                  f"  aslh (LUT {a[p]['lut']}, FF {a[p]['ff']})")
    only = sorted(set(e) ^ set(a))
    print(f"  rows present in one report only: {len(only)}")

    print("\n# wrapper KL_pp_shadow: total, own-cell row, children, total minus children (LUT, FF)")
    for n in reports:
        wp = "KL_pp_shadow" if n.startswith("ooc") else "alinx_ax7101/milan_datapath/pp_shadow"
        total, own, kids, ksum = wrapper(parsed[n], wp)
        print(f"  {n}: total ({total['lut']}, {total['ff']})  own-cell ({own['lut']}, {own['ff']})"
              f"  children {[k for k, _ in kids]} sum ({ksum['lut']}, {ksum['ff']})"
              f"  total-minus-children ({total['lut'] - ksum['lut']}, {total['ff'] - ksum['ff']})")

    print("\n# gate records' scopes, record 16 minus record 15 (LUT, FF)")
    j15 = json.loads(r15.read_text())["endpoints"]
    j16 = json.loads(r16.read_text())["endpoints"]
    for ep in ("route-1x1", "ooc-1x1", "ooc-8x8"):
        s15 = j15[ep]["record"]["scopes"]
        s16 = j16[ep]["record"]["scopes"]
        f15 = j15[ep]["record"]["figures"]
        f16 = j16[ep]["record"]["figures"]
        print(f"  {ep}: figures LUT {f15.get('LUT')} -> {f16.get('LUT')}, FF {f15.get('FF')} -> {f16.get('FF')}")
        deltas = {}
        for scope in ("wrapper", "u_pp", "ctl_fifo", "u_nvm"):
            a15, a16 = s15[scope], s16[scope]
            deltas[scope] = (a16["LUT"] - a15["LUT"], a16["FF"] - a15["FF"])
            print(f"    {scope}: LUT {a15['LUT']} -> {a16['LUT']} ({deltas[scope][0]:+d}),"
                  f" FF {a15['FF']} -> {a16['FF']} ({deltas[scope][1]:+d})")
        rest = tuple(deltas["wrapper"][i] - sum(deltas[s][i] for s in ("u_pp", "ctl_fifo", "u_nvm"))
                     for i in (0, 1))
        print(f"    change in the wrapper's remainder (wrapper less its three children): LUT {rest[0]:+d}, FF {rest[1]:+d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
