#!/usr/bin/env python3
# Minimal drawio -> SVG renderer for verification: reads mxCell vertices
# (rounded rects with wrapped labels) and edges (orthogonal arrows) and emits
# an SVG that faithfully mirrors the diagram geometry.
import sys, re, html
import xml.etree.ElementTree as ET

src, out = sys.argv[1], sys.argv[2]
root = ET.parse(src).getroot()
cells = {}
edges = []
for c in root.iter("mxCell"):
    g = c.find("mxGeometry")
    style = c.get("style", "") or ""
    val = c.get("value", "") or ""
    if c.get("vertex") == "1" and g is not None:
        cells[c.get("id")] = dict(
            x=float(g.get("x", 0)), y=float(g.get("y", 0)),
            w=float(g.get("width", 0)), h=float(g.get("height", 0)),
            label=val, style=style)
    elif c.get("edge") == "1":
        edges.append(dict(s=c.get("source"), t=c.get("target"), label=val,
                          dashed="dashed=1" in style and "endArrow=open" in style))

def sattr(style, key, dflt):
    m = re.search(rf"{key}=([^;]+)", style)
    return m.group(1) if m else dflt

W = max(c["x"]+c["w"] for c in cells.values()) + 40
H = max(c["y"]+c["h"] for c in cells.values()) + 40
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(W)}" height="{int(H)}" '
       f'viewBox="0 0 {int(W)} {int(H)}" font-family="Helvetica,Arial,sans-serif">',
       f'<rect width="{int(W)}" height="{int(H)}" fill="#ffffff"/>',
       '<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">'
       '<path d="M0,0 L7,3 L0,6 z" fill="#333"/></marker>'
       '<marker id="arro" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">'
       '<path d="M0,0 L7,3 L0,6" fill="none" stroke="#999"/></marker></defs>']

def center(c): return (c["x"]+c["w"]/2, c["y"]+c["h"]/2)
def anchor(a, b):
    # exit point on a's border toward b (orthogonal): pick side by dominant axis
    ax, ay = center(a); bx, by = center(b)
    if abs(bx-ax) >= abs(by-ay):
        x = a["x"]+a["w"] if bx > ax else a["x"]
        return (x, ay)
    else:
        y = a["y"]+a["h"] if by > ay else a["y"]
        return (ax, y)

# edges first (under boxes)
for e in edges:
    a, b = cells.get(e["s"]), cells.get(e["t"])
    if not a or not b: continue
    x1, y1 = anchor(a, b); x2, y2 = anchor(b, a)
    mx = (x1+x2)/2
    # orthogonal L/Z routing
    if abs(x1-x2) > 8 and abs(y1-y2) > 8:
        pts = f"M{x1},{y1} L{mx},{y1} L{mx},{y2} L{x2},{y2}"
    else:
        pts = f"M{x1},{y1} L{x2},{y2}"
    col = "#999" if e["dashed"] else "#333"
    dash = ' stroke-dasharray="4,3"' if e["dashed"] else ""
    mk = "arro" if e["dashed"] else "arr"
    svg.append(f'<path d="{pts}" fill="none" stroke="{col}" stroke-width="1.3"{dash} marker-end="url(#{mk})"/>')
    if e["label"]:
        svg.append(f'<text x="{mx}" y="{(y1+y2)/2-3}" font-size="10" fill="#555" '
                   f'text-anchor="middle">{html.escape(e["label"])}</text>')

def wrap(text, w, fs):
    # wrap on explicit \n and by width (~fs*0.55 px/char)
    cpl = max(6, int((w-12) / (fs*0.56)))
    out_lines = []
    for para in text.split("\n"):
        if not para:
            out_lines.append(""); continue
        line = ""
        for word in para.split(" "):
            if line and len(line)+1+len(word) > cpl:
                out_lines.append(line); line = word
            else:
                line = (line+" "+word).strip()
        out_lines.append(line)
    return out_lines

for cid, c in cells.items():
    fill = sattr(c["style"], "fillColor", "#ffffff")
    if fill == "none": fill = "none"
    stroke = sattr(c["style"], "strokeColor", "#333")
    fs = int(float(sattr(c["style"], "fontSize", "12")))
    rx = 8 if "rounded=1" in c["style"] else 0
    dash = ' stroke-dasharray="6,4"' if "dashed=1" in c["style"] else ""
    svg.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" rx="{rx}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="1.3"{dash}/>')
    bold = "fontStyle=1" in c["style"]
    va_top = "verticalAlign=top" in c["style"]
    al_left = "align=left" in c["style"]
    lines = wrap(c["label"], c["w"], fs)
    lh = fs + 3
    if va_top:
        ty = c["y"] + fs + 4
    else:
        ty = c["y"] + c["h"]/2 - (len(lines)-1)*lh/2 + fs*0.35
    for i, ln in enumerate(lines):
        if al_left or va_top:
            tx = c["x"]+8; anch = "start"
        else:
            tx = c["x"]+c["w"]/2; anch = "middle"
        fw = ' font-weight="bold"' if bold and i == 0 else ""
        svg.append(f'<text x="{tx}" y="{ty+i*lh}" font-size="{fs}" fill="#222" '
                   f'text-anchor="{anch}"{fw}>{html.escape(ln)}</text>')

svg.append("</svg>")
open(out, "w").write("\n".join(svg))
print("wrote", out)
