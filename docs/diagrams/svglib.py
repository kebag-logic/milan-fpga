"""Tiny SVG builder for the Milan perf docs — consistent styling, no deps.

Every drawing method takes its GEOMETRY positionally and EVERYTHING ELSE as
keywords, collected into one of the small style records below. Each record is
the single place a default lives, and a misspelt keyword is a `TypeError` out
of the record's constructor instead of a word that is silently ignored.

`box` is the one method whose geometry is itself a record — `Rect(x, y, w, h)`
— because it is the only one that is not a two-point line, and four bare
numbers in a row next to methods that read them as two corners is exactly the
transposition no reader can catch.
"""
from __future__ import annotations

from dataclasses import dataclass


def esc(t: object) -> str:
    """`t` as XML text with `&`, `<` and `>` neutralized, so no label can close a tag."""
    return str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")


def _marker(name, col):
    """One `col`-filled arrowhead, referenced as `url(#name)` by a line."""
    return (f'<marker id="{name}" markerWidth="10" markerHeight="10" refX="8" '
            f'refY="3" orient="auto">'
            f'<path d="M0,0 L8,3 L0,6 Z" fill="{col}"/></marker>')


def _dasharray(dash):
    """The `stroke-dasharray` attribute, or nothing when the stroke is solid."""
    return f' stroke-dasharray="{dash}"' if dash else ''


@dataclass(frozen=True)
class Rect:
    """`SVG.box`'s geometry: the top-left corner, then the size.

    One record rather than four adjacent floats, because a drawing API mixes
    two conventions — corner-and-size `(x, y, w, h)` and the two-corner
    `(x1, y1, x2, y2)` the line methods take — and four bare numbers in a row
    let a caller hand one to a method that wanted the other. That call is
    still legal Python and still draws a rectangle; it is simply the wrong
    one, and nothing before the render says so.
    """
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class BoxStyle:
    """`SVG.box`: the rectangle's paint, and the two text runs inside it."""
    fill: str = "#eef3f8"
    stroke: str = "#33628f"
    tcol: str = "#123"
    fs: float = 14
    r: float = 8
    dash: str | None = None
    sw: float = 1.6
    subcol: str = "#666"


@dataclass(frozen=True)
class LineStyle:
    """`SVG.line`: a plain rule."""
    col: str = "#ccc"
    w: float = 1
    dash: str | None = None


@dataclass(frozen=True)
class ArrowStyle:
    """`SVG.arrow`: a marker-ended line; `red` picks the red head AND colour."""
    col: str = "#555"
    w: float = 2
    red: bool = False
    dash: str | None = None


@dataclass(frozen=True)
class TextStyle:
    """`SVG.label`: one free-standing text run."""
    fs: float = 12
    col: str = "#444"
    anchor: str = "start"
    weight: str = "400"


class SVG:
    """An SVG document held as a list of elements, joined by `save`."""

    def __init__(s, w, h, title=None, sub=None):
        s.w, s.h = w, h; s.e = []
        s.e.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                   f'viewBox="0 0 {w} {h}" font-family="DejaVu Sans, Arial, sans-serif">')
        s.e.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
        s.e.append('<defs>' + _marker("arr", "#555")
                   + _marker("arrR", "#c0392b") + '</defs>')
        if title:
            s.e.append(f'<text x="{w/2}" y="34" text-anchor="middle" font-size="22" '
                       f'font-weight="700" fill="#111">{esc(title)}</text>')
        if sub:
            s.e.append(f'<text x="{w/2}" y="57" text-anchor="middle" font-size="13" '
                       f'fill="#666">{esc(sub)}</text>')

    def box(s: SVG, rect: Rect, label: str, sub: str | None = None,
            **style: str | float | None) -> None:
        """A rounded rectangle with `label` bold at its centre and `sub` under it.

        Both texts split on newlines into one centred run per line, so a caller
        writes the box's contents as one string rather than placing each line.
        """
        x, y, w, h = rect.x, rect.y, rect.w, rect.h
        st = BoxStyle(**style)
        d = _dasharray(st.dash)
        s.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{st.r}" '
                   f'fill="{st.fill}" stroke="{st.stroke}" stroke-width="{st.sw}"{d}/>')
        lines = label.split("\n"); n=len(lines)
        cy = y + h/2 - (n-1)*9 - (7 if sub else 0)
        for i,ln in enumerate(lines):
            s.e.append(f'<text x="{x+w/2}" y="{cy+i*18+5}" text-anchor="middle" '
                       f'font-size="{st.fs}" font-weight="700" '
                       f'fill="{st.tcol}">{esc(ln)}</text>')
        if sub:
            for j,sl in enumerate(sub.split("\n")):
                s.e.append(f'<text x="{x+w/2}" y="{cy+n*18+j*14+2}" text-anchor="middle" '
                           f'font-size="11" fill="{st.subcol}">{esc(sl)}</text>')

    def arrow(s: SVG, x1: float, y1: float, x2: float, y2: float,
              **style: str | float | bool | None) -> None:
        """A line ending in one of the two arrowheads `__init__` put in `<defs>`.

        The head is chosen by `red`, never by `col`, because a marker's fill is
        baked into its definition and cannot follow the stroke colour.
        """
        st = ArrowStyle(**style)
        d = _dasharray(st.dash)
        m = "url(#arrR)" if st.red else "url(#arr)"
        c = "#c0392b" if st.red else st.col
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" '
                   f'stroke-width="{st.w}" marker-end="{m}"{d}/>')

    def label(s: SVG, x: float, y: float, t: object, **style: str | float) -> None:
        """One free-standing text run; `anchor` decides whether `x` is its left
        edge, its centre or its right edge."""
        st = TextStyle(**style)
        s.e.append(f'<text x="{x}" y="{y}" text-anchor="{st.anchor}" '
                   f'font-size="{st.fs}" font-weight="{st.weight}" '
                   f'fill="{st.col}">{esc(t)}</text>')

    def line(s: SVG, x1: float, y1: float, x2: float, y2: float,
             **style: str | float | None) -> None:
        """A plain rule with no arrowhead - the axis ticks and the leader lines."""
        st = LineStyle(**style)
        d = _dasharray(st.dash)
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                   f'stroke="{st.col}" stroke-width="{st.w}"{d}/>')

    def save(s: SVG, path: str) -> str:
        """Close the document and write it to `path`, which is returned so the
        caller can report the file it just produced."""
        s.e.append('</svg>')
        with open(path,"w") as fh:
            fh.write("\n".join(s.e))
        return path
