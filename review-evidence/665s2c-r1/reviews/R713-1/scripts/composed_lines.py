"""Print each archived arm's composed-maximum lines. usage: composed_lines.py <arms-dir>"""
import sys
from pathlib import Path
for d in sorted(Path(sys.argv[1]).iterdir()):
    t = (d / 'table.md').read_text().splitlines()
    for line in t:
        if line.startswith(('Composed maximum', 'Over the windows', 'Partial', 'Worst pass', 'Composed ')) and not line.startswith('Composed windows'):
            print(f'{d.name}: {line}')
