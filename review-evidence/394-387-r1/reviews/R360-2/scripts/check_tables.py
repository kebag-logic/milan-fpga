#!/usr/bin/env python3
"""Count table cells in a markdown page and in a rendered HTML file.

Usage: check_tables.py <page.md> <rendered.html>
Exit 0 only if every markdown table has equal header/delimiter/row cell
counts and every rendered table has a uniform row width.
"""
import sys
from html.parser import HTMLParser


def md_cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, esc, code = [], "", False, False
    for ch in s:
        if esc:
            cur += ch
            esc = False
        elif ch == "\\":
            cur += ch
            esc = True
        elif ch == "`":
            code = not code
            cur += ch
        elif ch == "|":
            cells.append(cur)
            cur = ""
        else:
            cur += ch
    cells.append(cur)
    return len(cells)


def md_tables(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    tables, i = [], 0
    in_fence = False
    while i < len(lines):
        if lines[i].lstrip().startswith("```"):
            in_fence = not in_fence
        if (not in_fence and lines[i].lstrip().startswith("|") and i + 1 < len(lines)
                and set(lines[i + 1].replace("|", "").replace(":", "").replace("-", "").strip()) == set()
                and "-" in lines[i + 1]):
            start = i + 1
            rows = [md_cells(lines[i]), md_cells(lines[i + 1])]
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(md_cells(lines[i]))
                i += 1
            tables.append((start, rows))
            continue
        i += 1
    return tables


class T(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.row = [], None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tables.append([])
        elif tag == "tr":
            self.row = 0
        elif tag in ("td", "th") and self.row is not None:
            self.row += 1

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row)
            self.row = None


def main():
    md, html = sys.argv[1], sys.argv[2]
    ok = True
    mts = md_tables(md)
    print(f"markdown tables: {len(mts)}")
    for start, rows in mts:
        uniform = len(set(rows)) == 1
        ok &= uniform
        print(f"  line {start}: header={rows[0]} delimiter={rows[1]} rows={len(rows) - 2} "
              f"row-cells={sorted(set(rows[2:]))} {'OK' if uniform else 'MISMATCH'}")
    p = T()
    p.feed(open(html, encoding="utf-8").read())
    print(f"rendered tables: {len(p.tables)}")
    for n, t in enumerate(p.tables, 1):
        uniform = len(set(t)) == 1
        ok &= uniform
        print(f"  table {n}: rows={len(t)} cells={sorted(set(t))} {'OK' if uniform else 'MISMATCH'}")
    ok &= len(mts) == len(p.tables)
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
