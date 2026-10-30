"""copy_receipts.py <dest-dir> <file>...: copy text receipts into the output directory with host paths redacted
(<scratch> this round's scratch, <scratch-r2> round 2's, <lanes>, <tools>, <home>). A file over 200 KB is not
copied; its SHA-256 and size go to <dest-dir>/large.sha256 instead."""
import hashlib
import sys
from pathlib import Path

SUBS = [('$VALIDATION_STORAGE/scratch/814-a703c', '<scratch>'), ('$VALIDATION_STORAGE/scratch/814-a703b', '<scratch-r2>'),
        ('$VALIDATION_STORAGE/scratch', '<scratch-shared>'), ('$LANES', '<lanes>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$WORKSPACE_HOME', '<home>')]
dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
for name in sys.argv[2:]:
    src = Path(name)
    data = src.read_bytes()
    if len(data) > 200 * 1024:
        with (dest / 'large.sha256').open('a') as big:
            big.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {src.name}\n')
        continue
    text = data.decode('utf-8', 'replace')
    for old, new in SUBS:
        text = text.replace(old, new)
    (dest / src.name).write_text(text)
