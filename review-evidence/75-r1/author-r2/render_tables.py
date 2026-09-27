"""Render every table in supplied Markdown files and verify cell preservation.

Usage: python3 render_tables.py REPOSITORY OUTPUT_DIRECTORY MARKDOWN_FILE...
Uses the repository's pinned renderer and checks every row and cell.
"""
import hashlib
import json
from pathlib import Path
import sys


def main():
    repository, output = map(Path, sys.argv[1:3])
    sys.path.insert(0, str(repository/'scripts'))
    import gen_toc_renderer as renderer
    import cmarkgfm
    import html5lib
    renderer.render('# Renderer validation\n')
    receipts = []
    for filename in sys.argv[3:]:
        path = Path(filename)
        source = path.read_text()
        lines = source.splitlines()
        expected, table = [], []
        for line in lines + ['']:
            if line.startswith('|'):
                table.append(line)
            elif table:
                assert len(table) >= 2 and set(table[1]) <= set('|-: ')
                cells = [[cell.strip() for cell in line.strip('|').split('|')]
                         for line in [table[0]] + table[2:]]
                assert all(len(row) == len(cells[0]) for row in cells)
                expected.append(cells)
                table = []
        html = cmarkgfm.github_flavored_markdown_to_html(source)
        dom = html5lib.parse(html, namespaceHTMLElements=False)
        actual = list(dom.iter('table'))
        assert len(actual) == len(expected), 'table lost during rendering'
        counts = []
        for wanted, rendered in zip(expected, actual):
            rendered_rows = list(rendered.iter('tr'))
            assert len(rendered_rows) == len(wanted), 'row lost during rendering'
            for raw_cells, rendered_row in zip(wanted, rendered_rows):
                cells = [child for child in rendered_row if child.tag in ('th', 'td')]
                assert len(cells) == len(raw_cells), 'cell lost during rendering'
                for raw_cell, cell in zip(raw_cells, cells):
                    fragment = html5lib.parseFragment(cmarkgfm.github_flavored_markdown_to_html(raw_cell), namespaceHTMLElements=False)
                    expected_text = ''.join(fragment.itertext()).strip()
                    actual_text = ''.join(cell.itertext()).strip()
                    assert expected_text == actual_text, 'cell content changed during rendering'
            counts.append(dict(columns=len(wanted[0]), body_rows=len(wanted)-1))
        label = str(path.resolve().relative_to(repository.resolve())) if path.resolve().is_relative_to(repository.resolve()) else f'addendum/{path.name}'
        receipt = dict(file=label, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), tables=counts, result='PASS')
        receipts.append(receipt)
        print(f'{path.name}: PASS, {len(counts)} tables, {sum(r["body_rows"] for r in counts)} body rows')
    (output/'table-render-check.json').write_text(json.dumps(receipts, indent=2)+'\n')


if __name__ == '__main__':
    main()
