#!/usr/bin/env python3
"""Create review images and a machine-readable graph inventory.

Usage: python3 scripts/inspect_graphs.py PACKET
"""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

packet = Path(sys.argv[1]).resolve()
out = packet / "diagrams"
out.mkdir(exist_ok=True)

def render(path):
    svg = ET.parse(path.with_suffix(".svg")).getroot()
    target = out / (path.stem + ".png")
    cmd = ["mmdc", "-i", str(path), "-o", str(target), "-b", "white", "-w", "1400"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    source = path.read_text()
    if source.startswith("sequenceDiagram"):
        labels = [s.split(":", 1)[1].strip() for s in source.splitlines() if ":" in s]
    elif source.startswith("stateDiagram"):
        labels = [s.split(":", 1)[1].strip() for s in source.splitlines() if ":" in s]
    else:
        labels = re.findall(r"\[([^\]]+)\]", source)
    direction = "sequence" if source.startswith("sequenceDiagram") else ("LR" if " LR" in source else "TD")
    return dict(graph=path.stem, source=source, rc=r.returncode, viewBox=svg.attrib["viewBox"],
                direction=direction, max_label_characters=max(map(len,labels)),
                max_label_words=max(len(s.split()) for s in labels), image=target.name)

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(render, sorted((packet / "graphs").glob("*.mmd"))))
(packet / "receipts/graph-inventory.json").write_text(json.dumps(results, indent=2) + "\n")
# These sheets are navigation aids; individual images retain their original dimensions.
for offset in range(0, len(results), 4):
    sheet = Image.new("RGB", (1600, 1600), "white")
    draw = ImageDraw.Draw(sheet)
    for n, row in enumerate(results[offset:offset+4]):
        im = Image.open(out / row["image"]).convert("RGB")
        im.thumbnail((780, 745))
        x, y = n % 2 * 800, n // 2 * 800
        draw.text((x+10, y+10), row["graph"], fill="black")
        sheet.paste(im, (x+(800-im.width)//2, y+40))
    sheet.save(out / ("sheet-%02d.png" % (offset//4+1)))
print(json.dumps([{k:v for k,v in row.items() if k != "source"} for row in results], indent=2))
