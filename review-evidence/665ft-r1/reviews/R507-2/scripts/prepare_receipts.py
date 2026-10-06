#!/usr/bin/env python3
"""Remove private installation prefixes, retaining the original under scratch.

Only a compiler's embedded installation prefix is replaced. Test output,
commands, versions, executable hashes and return codes are preserved.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

packet = Path(sys.argv[1]).resolve()
published = packet / 'receipts/mailbox.log'
raw = packet / 'scratch/mailbox.original.log'
if not raw.exists():
    raw.write_bytes(published.read_bytes())
original = raw.read_bytes()
text, count = re.subn(rb'/home/[^\s]+?/diff/usr/share/verilator', b'<simulator-root>', original)
assert count > 0
assert b'/home/' not in text
published.write_bytes(text)
record = {
    'receipt': 'receipts/mailbox.log',
    'transformation': 'Only private installation prefixes replaced with <simulator-root>; original retained in unpublished scratch.',
    'replacement_count': count,
    'original_sha256': hashlib.sha256(original).hexdigest(),
    'published_sha256': hashlib.sha256(text).hexdigest(),
}
(packet / 'receipts/path-redaction.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
