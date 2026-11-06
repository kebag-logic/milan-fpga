#!/usr/bin/env python3
"""Copy text files into a receipts subdirectory with host paths redacted (collect.py's substitutions); a file whose
redacted text is over 200 KB is kept off, its sha256 and size recorded instead.
usage: redact_copy.py SUBDIR FILE [FILE...]"""
import hashlib
import sys
from pathlib import Path

sys.argv[0:0] = []
R = Path('$MANAGEMENT/2026-09-23/665s2b-a683u/receipts')
SUBS = [('$VALIDATION_STORAGE/665s2b-a683u', '<scratch>'), ('$VALIDATION_STORAGE', '<tmp>'), ('$LANES', '<lanes>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$VALIDATION_STORAGE/scratch', '<tools>'), ('/srv/act-slots', '<slots>'),
        ('$WORKSPACE_HOME', '$HOME')]
out = R / sys.argv[1]
out.mkdir(parents=True, exist_ok=True)
for name in sys.argv[2:]:
    p = Path(name)
    text = p.read_text(errors='replace')
    for a, b in SUBS:
        text = text.replace(a, b)
    data = text.encode()
    if len(data) > 200_000:
        (out / f'{p.name}.sha256').write_text(f'{hashlib.sha256(data).hexdigest()}  {len(data)} B redacted '
                                              f'(over 200 KB, kept off)\n')
    else:
        (out / p.name).write_bytes(data)
    print(out.name, p.name, len(data))
