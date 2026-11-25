#!/usr/bin/env python3
"""Check the route receipts: source binding against git, repo inputs against checkout bytes, and every corner's figures.

usage: route_check.py RECEIPTS REPO HEAD
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
R, repo, head = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
git = lambda *a: subprocess.check_output(["/usr/bin/git", "-C", str(repo), *a], text=True).strip()
def body(p):
    t = p.read_text(errors="replace"); i = t.find("{")
    return json.loads(t[i:])
b = body(R / "source-binding.json.txt")
for k in ("identity_start", "identity_end"):
    d = b[k]; ok = d["head"] == git("rev-parse", head) and d["tree"] == git("rev-parse", head + "^{tree}") and not d["dirty_tracked"]
    ok &= all(git("rev-parse", f"{head}:{n}") == v for n, v in d["trees"].items())
    ok &= all(git("rev-parse", f"{head}:{n}") == v for n, v in d["gitlinks"].items())
    ok &= all(d["gitlinks"][n] == v for n, v in d["submodule_heads"].items()) and not any(d["submodule_dirty"].values())
    print(k, "binding", "ok" if ok else "BAD")
for c in ("1x1_tdm8", "8x8"):
    t = (R / f"inputs-endstation_ax7101_{c}.json.txt").read_text(); j = json.loads(t[t.find("{"):])
    pairs = []
    def walk(o):
        if isinstance(o, dict):
            p = o.get("path") or o.get("file"); h = o.get("sha256")
            if isinstance(p, str) and isinstance(h, str): pairs.append((p, h))
            for k, v in o.items():
                if isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) and k != "sha256": pairs.append((k, v))
                walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(j)
    n = bad = skip = 0
    for p, h in sorted(set(pairs)):
        m = re.search(r"((?:hdl|sw|configs|tb|syn|third_party|gptp-processor|protocol-processor)/.*)$", p)
        f = repo / m.group(1) if m else None
        if f and f.is_file() and subprocess.run(["/usr/bin/git", "-C", str(f.parent), "ls-files", "--error-unmatch", f.name], capture_output=True).returncode == 0:
            n += 1
            if hashlib.sha256(f.read_bytes()).hexdigest() != h: bad += 1; print("  BAD", p)
        else: skip += 1
    print(c, "inputs: tracked checked", n, "bad", bad, "generated/other", skip)
names = sorted({m.group(1) for f in R.iterdir() if (m := re.match(r"(route-(?:1x1|8x8)--\w+)--", f.name))})
for n in names:
    row = []
    for corner in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C"):
        parts = sorted(R.glob(f"{n}--alinx_ax7101_signoff_{corner}_timing.rpt*.txt"))
        t = "".join(p.read_text(errors="replace") for p in parts)
        m = re.search(r"WNS\(ns\).*?\n\s*-[- ]+\n\s*(-?[\d.]+)\s+(-?[\d.]+)\s+(\d+)\s+(\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(\d+)\s+(\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(\d+)\s+(\d+)", t)
        g = m.groups(); row.append(f"{corner} WNS {g[0]} fail {g[2]} WHS {g[4]} fail {g[6]} WPWS {g[8]} fail {g[10]}")
    s = (R / f"{n}--alinx_ax7101_route_status.rpt.txt").read_text()
    rs = re.findall(r"# of (routable nets|fully routed nets|nets with routing errors)\.*\s*:\s*(\d+)", s)
    u = (R / f"{n}--routed_util.rpt.txt").read_text()
    uf = {k: re.search(r"\|\s*" + k + r"\s*\|\s*([\d.]+)", u) for k in ("Slice LUTs", "Slice Registers", "Block RAM Tile", "DSPs", "Slice ")}
    print(n, "|", "; ".join(row), "|", rs, {k: v.group(1) for k, v in uf.items() if v})
