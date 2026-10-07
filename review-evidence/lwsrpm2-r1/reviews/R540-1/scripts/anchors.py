# SPDX-License-Identifier: Apache-2.0
"""Print every Markdown source-line anchor with the text of its target lines."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
for md in sorted(list(root.glob('*.md')) + list(root.glob('doc/*.md'))):
    text = md.read_text()
    for n, line in enumerate(text.splitlines(), 1):
        for label, target, a, b in re.findall(r'\[([^\]]+)\]\(([^)#]+)#L(\d+)(?:-L(\d+))?\)', line):
            path = (md.parent / target).resolve()
            lines = path.read_text().splitlines()
            lo, hi = int(a), int(b or a)
            body = ' | '.join(l.strip() for l in lines[lo - 1:hi])[:110]
            print(f"{md.relative_to(root)}:{n} [{label}] -> {target}#L{a}{'-L'+b if b else ''}: {body}")
