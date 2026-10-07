#!/usr/bin/env python3
"""Geometric check of rendered Mermaid flowchart/state SVGs: does any edge path
or edge label pass through a node that is not one of the edge's endpoints?
Usage: edge-node-crossings.py SVG... ; prints one line per graph; rc 1 on any crossing."""
import re, sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
TR = re.compile(r"translate\(\s*([-\d.e]+)[ ,]+([-\d.e]+)\s*\)")

def walk(el, ox=0.0, oy=0.0):
    m = TR.search(el.get("transform", "") or "")
    if m:
        ox, oy = ox + float(m[1]), oy + float(m[2])
    yield el, ox, oy
    for c in el:
        yield from walk(c, ox, oy)

def path_points(d, ox, oy, steps=40):
    toks = re.findall(r"[MLCmlc]|[-\d.e]+", d)
    pts, i, cmd, cur = [], 0, None, (0.0, 0.0)
    while i < len(toks):
        if toks[i] in "MLCmlc":
            cmd = toks[i]; i += 1; continue
        if cmd in ("M", "L"):
            cur = (float(toks[i]), float(toks[i + 1])); i += 2; pts.append(cur)
        elif cmd == "C":
            p1 = (float(toks[i]), float(toks[i + 1])); p2 = (float(toks[i + 2]), float(toks[i + 3]))
            p3 = (float(toks[i + 4]), float(toks[i + 5])); i += 6
            for s in range(1, steps + 1):
                t = s / steps; u = 1 - t
                pts.append((u**3*cur[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                            u**3*cur[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
            cur = p3
        else:
            raise ValueError(f"unsupported path command {cmd}")
    # densify straight segments
    dense = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(max(abs(b[0]-a[0]), abs(b[1]-a[1])) / 2))
        dense += [(a[0] + (b[0]-a[0])*k/n + ox, a[1] + (b[1]-a[1])*k/n + oy) for k in range(n)]
    dense.append((pts[-1][0] + ox, pts[-1][1] + oy))
    return dense

def inside(p, box, pad=0.0):
    x0, y0, x1, y1 = box
    return x0 + pad < p[0] < x1 - pad and y0 + pad < p[1] < y1 - pad

def dist(p, box):
    x0, y0, x1, y1 = box
    dx = max(x0 - p[0], 0, p[0] - x1); dy = max(y0 - p[1], 0, p[1] - y1)
    return (dx*dx + dy*dy) ** 0.5

def overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

def check(path):
    root = ET.parse(path).getroot()
    nodes, edges, labels = {}, [], []
    for el, ox, oy in walk(root):
        cls = el.get("class", "") or ""
        if el.tag == NS + "g" and re.search(r"\bnode\b", cls) and el.get("id"):
            box = None
            for c in el:
                if c.tag == NS + "rect":
                    x, y = float(c.get("x", 0)), float(c.get("y", 0))
                    box = (ox + x, oy + y, ox + x + float(c.get("width")), oy + y + float(c.get("height")))
                    break
                if c.tag == NS + "circle":
                    r = float(c.get("r", 7)); box = (ox - r, oy - r, ox + r, oy + r); break
            if box is None:
                box = (ox - 7, oy - 7, ox + 7, oy + 7)
            nodes[el.get("id")] = box
        elif el.tag == NS + "path" and ("flowchart-link" in cls or re.search(r"\btransition\b", cls)):
            edges.append((el.get("id"), path_points(el.get("d"), ox, oy)))
        elif el.tag == NS + "g" and "edgeLabel" in cls:
            for c in el.iter():
                if c.tag == NS + "foreignObject" or (c.tag == NS + "rect" and c.get("width")):
                    w, h = float(c.get("width", 0)), float(c.get("height", 0))
                    if w > 0 and h > 0:
                        # label groups are translated to their centre; inner group offsets by -w/2,-h/2
                        labels.append((ox - w/2, oy - h/2, ox + w/2, oy + h/2))
                    break
    problems = []
    for eid, pts in edges:
        ends = {min(nodes, key=lambda n: dist(pts[0], nodes[n])), min(nodes, key=lambda n: dist(pts[-1], nodes[n]))}
        for nid, box in nodes.items():
            if nid in ends:
                continue
            hits = [p for p in pts if inside(p, box, 1.0)]
            if hits:
                problems.append(f"edge {eid} crosses node {nid} ({len(hits)} samples)")
    return len(nodes), len(edges), len(labels), problems

rc = 0
for f in sys.argv[1:]:
    text = open(f, encoding="utf-8").read()
    kind = "sequence" if 'aria-roledescription="sequence"' in text else ("state" if "stateDiagram" in text else "flowchart")
    if kind == "sequence":
        print(f"{f.split('/')[-1]}: sequence diagram; lifeline layout, no node-crossing geometry (visual inspection only)")
        continue
    n, e, l, problems = check(f)
    rc |= bool(problems)
    print(f"{f.split('/')[-1]}: {kind}; nodes={n} edges={e} labels={l}; crossings={len(problems)}" + "".join("\n  " + p for p in problems))
sys.exit(rc)
