#!/usr/bin/env python3
"""Tabulate receipts/size/*.json: sections, static storage and deltas (head vs base, r5, r6).
usage: r532_7_size_table.py PACKET  -> prints a markdown table and writes receipts/size/TABLE.md"""
import json
import sys
from pathlib import Path

z = Path(sys.argv[1]) / "receipts/size"
rows = []
for shape in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    for n in (1, 2):
        get = {t: json.loads((z / f"{t}-{shape}-if{n}.json").read_text()) for t in ("head", "r6", "r5", "base")}
        h = get["head"]
        s = h["sections"]
        st = {t: get[t]["static_storage"] for t in get}
        sec = {t: get[t]["sections"] for t in get}
        rows.append(f"| {shape.split('_')[2]} / {n} | {s['.text']} | {s['.rodata']} | {s.get('.data', 0)} | {s['.bss']} | "
                    f"{h['ram_span']} | {h['ram_span'] - get['base']['ram_span']:+d} | "
                    f"{h['ram_span'] - get['r5']['ram_span']:+d} | {h['ram_span'] - get['r6']['ram_span']:+d} | "
                    f"{s['.text'] - sec['r6']['.text']:+d} | {s['.bss'] - sec['r6']['.bss']:+d} | "
                    f"{st['head'].get('image_srp', 0) - st['r6'].get('image_srp', 0):+d} | "
                    f"{st['head'].get('image_app', 0) - st['r5'].get('image_app', 0):+d} | "
                    f"{st['head'].get('image_srp', 0) - st['r5'].get('image_srp', 0):+d} | "
                    f"{s['.text'] - sec['r5']['.text']:+d} |")
head = ("| Shape / IF | Text | Rodata | Data | BSS | RAM span | vs base | vs R5 | vs R6 | text vs R6 | BSS vs R6 | "
        "image_srp vs R6 | image_app vs R5 | image_srp vs R5 | text vs R5 |\n|" + "---|" * 15 + "\n")
table = head + "\n".join(rows) + "\n"
(z / "TABLE.md").write_text(table)
print(table)
for t in ("head", "r6", "r5", "base"):
    print(t, json.loads((z / f"{t}-endstation_ax7101_1x1_tdm8-if1.json").read_text())["static_storage"])
