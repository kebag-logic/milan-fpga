"""Tiny SVG builder for the Milan perf docs — consistent styling, no deps."""
def esc(t):
    return str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
class SVG:
    def __init__(s, w, h, title=None, sub=None):
        s.w, s.h = w, h; s.e = []
        s.e.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="DejaVu Sans, Arial, sans-serif">')
        s.e.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
        s.e.append('<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#555"/></marker>'
                   '<marker id="arrR" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#c0392b"/></marker></defs>')
        if title: s.e.append(f'<text x="{w/2}" y="34" text-anchor="middle" font-size="22" font-weight="700" fill="#111">{esc(title)}</text>')
        if sub:   s.e.append(f'<text x="{w/2}" y="57" text-anchor="middle" font-size="13" fill="#666">{esc(sub)}</text>')
    def box(s, x, y, w, h, label, sub=None, fill="#eef3f8", stroke="#33628f", tcol="#123", fs=14, r=8, dash=None, sw=1.6, subcol="#666"):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
        lines = label.split("\n"); n=len(lines)
        cy = y + h/2 - (n-1)*9 - (7 if sub else 0)
        for i,ln in enumerate(lines):
            s.e.append(f'<text x="{x+w/2}" y="{cy+i*18+5}" text-anchor="middle" font-size="{fs}" font-weight="700" fill="{tcol}">{esc(ln)}</text>')
        if sub:
            for j,sl in enumerate(sub.split("\n")):
                s.e.append(f'<text x="{x+w/2}" y="{cy+n*18+j*14+2}" text-anchor="middle" font-size="11" fill="{subcol}">{esc(sl)}</text>')
    def arrow(s, x1,y1,x2,y2, col="#555", w=2, red=False, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        m = "url(#arrR)" if red else "url(#arr)"
        c = "#c0392b" if red else col
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="{m}"{d}/>')
    def label(s, x, y, t, fs=12, col="#444", anchor="start", weight="400"):
        s.e.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" font-weight="{weight}" fill="{col}">{esc(t)}</text>')
    def line(s, x1,y1,x2,y2, col="#ccc", w=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d}/>')
    def save(s, path):
        s.e.append('</svg>'); open(path,"w").write("\n".join(s.e)); return path
