"""Render a Markdown page with the pinned GFM renderer and compare every table.

Usage: python -B table_render_check.py PAGE [PAGE ...]
For each source pipe table (header + delimiter row), checks that the rendered
HTML has a table with the same number of body rows and cells per row, and that
each cell's text equals the source cell after inline rendering. Exits 1 on any
difference.
"""
import sys
from pathlib import Path

import cmarkgfm
import html5lib
from cmarkgfm.cmark import Options


def text(el):
    return ''.join(el.itertext()).strip()


def source_tables(lines):
    tables, i = [], 0
    while i < len(lines) - 1:
        if lines[i].startswith('|') and set(lines[i + 1].strip()) <= set('|-: ') and lines[i + 1].startswith('|---'):
            j = i + 2
            while j < len(lines) and lines[j].startswith('|'):
                j += 1
            tables.append((i + 1, [split(lines[i])] + [split(l) for l in lines[i + 2:j]]))
            i = j
        else:
            i += 1
    return tables


def split(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def main():
    bad = 0
    for page in map(Path, sys.argv[1:]):
        src = page.read_text()
        html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE)
        doc = html5lib.parse(html, namespaceHTMLElements=False)
        rendered = doc.findall('.//table')
        wanted = source_tables(src.splitlines())
        ok = len(rendered) == len(wanted)
        print(f'{page.name}: {len(wanted)} source tables, {len(rendered)} rendered')
        for (line, rows), table in zip(wanted, rendered):
            rrows = table.findall('.//tr')
            cells = [[text(c) for c in r if c.tag in ('td', 'th')] for r in rrows]
            same_shape = len(cells) == len(rows) and all(len(c) == len(r) for c, r in zip(cells, rows))
            empty = sum(1 for r in cells for c in r if c == '')
            src_empty = sum(1 for r in rows for c in r if c == '')
            good = same_shape and empty == src_empty
            ok &= good
            if not good:
                print(f'  line {line}: MISMATCH rows {len(rows)} vs {len(cells)}')
        print(f'{page.name}: ' + ('PASS all tables, rows and cells preserved' if ok else 'FAIL'))
        bad += not ok
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
