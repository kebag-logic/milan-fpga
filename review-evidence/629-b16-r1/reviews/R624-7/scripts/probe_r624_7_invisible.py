#!/usr/bin/env python3
"""R624-7: invisible format characters between an identifier's digit and a unit (offline, copies only).
usage: python3 -I probe_r624_7_invisible.py <repo at head> <author-r7 packet> <work dir> <out.json>"""
import json, subprocess, sys
from pathlib import Path
repo, packet, work, out = (Path(a).resolve() for a in sys.argv[1:5])
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
orig = page.read_text(encoding="utf-8")
needle = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
CH = {"U+2061": "⁡", "U+2062": "⁢", "U+2063": "⁣", "U+2064": "⁤", "U+034F": "͏",
      "U+180E": "᠎", "U+2066_2069": "⁦⁩", "U+200E": "‎", "U+00AD": "­", "U+3164": "ㅤ"}
res = []
for name, c in CH.items():
    d = work / name.replace("+", "")
    d.mkdir(parents=True, exist_ok=True)
    (d / page.name).write_text(orig.replace(needle, needle + f" CLOCK_DOMAIN 7{c}ppm."), encoding="utf-8")
    (d / "README.md").write_bytes((page.parent / "README.md").read_bytes())
    p = subprocess.run([sys.executable, "-I", str(packet / "tools/check_b16_figures.py"), str(d / page.name), str(packet),
                        str(d / "r.tsv"), str(d / "c.tsv"), "--repo", str(repo)], capture_output=True, text=True, timeout=300)
    res.append(dict(form=name, rc=p.returncode, named=[x[:200] for x in p.stdout.splitlines()[1:3]]))
    print(name, p.returncode)
json.dump(res, open(out, "w"), indent=1)
