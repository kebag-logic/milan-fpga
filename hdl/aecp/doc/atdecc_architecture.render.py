#!/usr/bin/env python3
# Minimal drawio -> SVG renderer used to VERIFY the diagram renders correctly
# (drawio headless needs a display). Handles every <diagram> page in the file:
#   atdecc_architecture.svg / .png                 = page 1 (overview)
#   atdecc_architecture.<page-name>.svg / .png     = detail pages
# Usage: python3 atdecc_architecture.render.py [file.drawio]
# PNGs are produced with rsvg-convert when available.
import sys, re, html, os, subprocess
import xml.etree.ElementTree as ET

src = sys.argv[1] if len(sys.argv) > 1 else "atdecc_architecture.drawio"
stem = os.path.splitext(src)[0]
root = ET.parse(src).getroot()

def sattr(style, key, dflt):
    m = re.search(rf"{key}=([^;]+)", style)
    return m.group(1) if m else dflt

def render_page(model, out):
    cells, edges = {}, []
    for c in model.iter("mxCell"):
        g = c.find("mxGeometry")
        style = c.get("style", "") or ""
        val = c.get("value", "") or ""
        if c.get("vertex") == "1" and g is not None:
            cells[c.get("id")] = dict(
                x=float(g.get("x", 0)), y=float(g.get("y", 0)),
                w=float(g.get("width", 0)), h=float(g.get("height", 0)),
                label=val, style=style, parent=c.get("parent", "1"))
        elif c.get("edge") == "1":
            def frac(k):
                m = re.search(rf"{k}=([0-9.]+)", style)
                return float(m.group(1)) if m else None
            vx = vy = None
            arr = c.find("mxGeometry/Array")
            if arr is not None:
                pt = arr.find("mxPoint")
                if pt is not None:
                    vx = float(pt.get("x")) if pt.get("x") else None
                    vy = float(pt.get("y")) if pt.get("y") else None
            edges.append(dict(s=c.get("source"), t=c.get("target"), label=val,
                              dashed="dashed=1" in style,
                              open="endArrow=open" in style,
                              w=float(sattr(style, "strokeWidth", "1.6")),
                              color=sattr(style, "strokeColor", "#333333"),
                              ex=frac("exitX"), ey=frac("exitY"),
                              nx=frac("entryX"), ny=frac("entryY"),
                              vx=vx, vy=vy))

    # resolve nested coordinates (child x/y are relative to the parent).
    # Resolve from a SNAPSHOT of the original relative coords — resolving
    # in place makes grandchildren add their grandparent twice.
    orig = {cid: (c["x"], c["y"], c.get("parent", "1")) for cid, c in cells.items()}
    memo = {}
    def absxy(cid, seen=()):
        if cid in memo: return memo[cid]
        x, y, p = orig[cid]
        if p in orig and p not in seen and p != cid:
            px, py = absxy(p, seen + (cid,))
            memo[cid] = (x + px, y + py)
        else:
            memo[cid] = (x, y)
        return memo[cid]
    for cid in list(cells):
        cells[cid]["x"], cells[cid]["y"] = absxy(cid)

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
        # exit point on a's border toward b (orthogonal): side by dominant axis
        ax, ay = center(a); bx, by = center(b)
        if abs(bx-ax) >= abs(by-ay):
            x = a["x"]+a["w"] if bx > ax else a["x"]
            return (x, ay)
        else:
            y = a["y"]+a["h"] if by > ay else a["y"]
            return (ax, y)

    def wrap(text, w, fs, mono):
        # \n are hard breaks (authored as &#10; in the file, preserved by the
        # XML parser). Mono boxes are pre-formatted tables: never re-wrap.
        cpl = max(6, int((w-12) / (fs * (0.62 if mono else 0.56))))
        out_lines = []
        for para in text.split("\n"):
            if not para or mono:
                out_lines.append(para); continue
            line = ""
            for word in para.split(" "):
                if line and len(line)+1+len(word) > cpl:
                    out_lines.append(line); line = word
                else:
                    line = (line+" "+word) if line else word
            out_lines.append(line)
        return out_lines

    for cid, c in cells.items():
        fill = sattr(c["style"], "fillColor", "#ffffff")
        stroke = sattr(c["style"], "strokeColor", "#333")
        fs = int(float(sattr(c["style"], "fontSize", "12")))
        mono = "Courier" in c["style"]
        rx = 8 if "rounded=1" in c["style"] else 0
        dash = ' stroke-dasharray="6,4"' if "dashed=1" in c["style"] else ""
        svg.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" rx="{rx}" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="1.3"{dash}/>')
        bold = "fontStyle=1" in c["style"]
        va_top = "verticalAlign=top" in c["style"]
        al_left = "align=left" in c["style"]
        lines = wrap(c["label"], c["w"], fs, mono)
        lh = fs + 3
        if va_top:
            ty = c["y"] + fs + 4
        else:
            ty = c["y"] + c["h"]/2 - (len(lines)-1)*lh/2 + fs*0.35
        fam = ' font-family="Courier New,monospace"' if mono else ""
        for i, ln in enumerate(lines):
            if al_left or va_top:
                tx = c["x"]+8; anch = "start"
            else:
                tx = c["x"]+c["w"]/2; anch = "middle"
            fw = ' font-weight="bold"' if bold and i == 0 else ""
            svg.append(f'<text x="{tx}" y="{ty+i*lh}" font-size="{fs}" fill="#222" '
                       f'text-anchor="{anch}"{fw}{fam}>{html.escape(ln)}</text>')

    # edges LAST (containers would paint over them)
    for e in edges:
        a, b = cells.get(e["s"]), cells.get(e["t"])
        if not a or not b: continue
        # pinned anchors (drawio exitX/entryX fractions) win over auto sides
        if e["ex"] is not None:
            x1 = a["x"] + a["w"] * e["ex"]; y1 = a["y"] + a["h"] * (e["ey"] or 0.5)
            v1 = e["ey"] in (0.0, 1.0)
        else:
            x1, y1 = anchor(a, b); v1 = False
        if e["nx"] is not None:
            x2 = b["x"] + b["w"] * e["nx"]; y2 = b["y"] + b["h"] * (e["ny"] or 0.5)
            v2 = e["ny"] in (0.0, 1.0)
        else:
            x2, y2 = anchor(b, a); v2 = False
        if e.get("vy") is not None:      # explicit horizontal shelf
            vy = e["vy"]
            pts = f"M{x1},{y1} L{x1},{vy} L{x2},{vy} L{x2},{y2}"
        elif e.get("vx") is not None:    # explicit vertical shelf
            vx = e["vx"]
            pts = f"M{x1},{y1} L{vx},{y1} L{vx},{y2} L{x2},{y2}"
        elif abs(x1-x2) <= 8 or abs(y1-y2) <= 8:
            pts = f"M{x1},{y1} L{x2},{y2}"
        elif v1 and v2:      # vertical out, vertical in: V-H-V through mid-y
            my = (y1+y2)/2
            pts = f"M{x1},{y1} L{x1},{my} L{x2},{my} L{x2},{y2}"
        elif v1:             # vertical out, horizontal in
            pts = f"M{x1},{y1} L{x1},{y2} L{x2},{y2}"
        elif v2:             # horizontal out, vertical in
            pts = f"M{x1},{y1} L{x2},{y1} L{x2},{y2}"
        else:                # H-V-H through mid-x
            mx0 = (x1+x2)/2
            pts = f"M{x1},{y1} L{mx0},{y1} L{mx0},{y2} L{x2},{y2}"
        mx, myl = (x1+x2)/2, (y1+y2)/2
        col = e["color"] if not e["open"] else "#999"
        dash = ' stroke-dasharray="6,4"' if e["dashed"] else ""
        mk = "arro" if e["open"] else "arr"
        svg.append(f'<path d="{pts}" fill="none" stroke="{col}" stroke-width="{e["w"]}"{dash} marker-end="url(#{mk})"/>')
        if e["label"]:
            lw = len(e["label"]) * 6.2 + 8
            ly = myl
            svg.append(f'<rect x="{mx-lw/2}" y="{ly-12}" width="{lw}" height="15" '
                       f'fill="#ffffff" fill-opacity="0.92" stroke="none"/>')
            svg.append(f'<text x="{mx}" y="{ly}" font-size="10" fill="#444" '
                       f'text-anchor="middle">{html.escape(e["label"])}</text>')

    svg.append("</svg>")
    open(out, "w").write("\n".join(svg))
    return out

outs = []
for n, d in enumerate(root.findall("diagram"), start=1):
    model = d.find("mxGraphModel")
    if model is None:      # compressed pages unsupported (we always write plain)
        continue
    name = d.get("name", f"p{n}")
    out = f"{stem}.svg" if n == 1 else f"{stem}.{name}.svg"
    outs.append(render_page(model, out))

for o in outs:
    png = o[:-4] + ".png"
    try:
        subprocess.run(["rsvg-convert", "-o", png, "-b", "white", "--zoom", "1.6", o],
                       check=True)
    except Exception as e:
        print("png skipped:", e)
        break
print("rendered", len(outs), "pages:", ", ".join(os.path.basename(o) for o in outs))
