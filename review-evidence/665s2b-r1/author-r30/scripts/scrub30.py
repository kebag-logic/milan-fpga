"""Replace host paths in receipt text files with placeholders (in place), refusing files over 200 KB."""
import sys
from pathlib import Path
SUBS = [('/data-2/milan/tmp/665s2b-a683zo', '<scratch>'),
        ('$LANES/665-s2b-cycles', '<lane>'), ('$LANES', '<lanes>'),
        ('$MANAGEMENT', '<management>'), ('$VALIDATION_TOOLS', '<tools>'),
        ('$WORKSPACE_HOME', '<home>'), ('/data-2/milan/tmp', '<tmp>'), ('$VALIDATION_STORAGE', '<data>')]
for root in sys.argv[1:]:
    for p in Path(root).rglob('*'):
        if not p.is_file():
            continue
        b = p.read_bytes()
        if len(b) > 200_000:
            raise SystemExit(f'over 200 KB: {p}')
        try:
            t = b.decode()
        except UnicodeDecodeError:
            continue
        n = t
        for a, r in SUBS:
            n = n.replace(a, r)
        if n != t:
            p.write_text(n)
