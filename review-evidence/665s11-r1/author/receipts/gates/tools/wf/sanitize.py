#!/usr/bin/env python3
"""sanitize.py <table.tsv> <file>...: replace each host prefix of the table with its placeholder, in place."""
import sys
from pathlib import Path

pairs = [line.split("\t") for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
for name in sys.argv[2:]:
    path = Path(name)
    text = path.read_text()
    for old, new in pairs:
        text = text.replace(old, new)
    path.write_text(text)
