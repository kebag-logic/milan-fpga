#!/usr/bin/env python3
"""File a directory of gate logs into the packet: each file copied with host paths replaced by placeholders (scrub.py's
SUBS); a file over 190 KB excerpted (its first and last 300 lines) and its raw size and sha256 recorded in the
packet's raw-manifest.json, so a reader can match the excerpt to the raw log the gate wrote.
usage: file_receipts.py SRC_DIR DST_DIR PACKET_ROOT [GLOB]"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
SUBS = (('/data-2/milan/tmp/894b-a781', '$SCRATCH'), ('$WORKSPACE_HOME', '$HOME'), ('/data-2/milan', '/<data-2>'),
        ('$VALIDATION_STORAGE', '/<data>'), ('hackerman-kl', '<account>'), ('/tmp/', '/<tmp>/'))
src, dst, root = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
pattern = sys.argv[4] if len(sys.argv) > 4 else '*'
manifest_path = root / 'raw-manifest.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
dst.mkdir(parents=True, exist_ok=True)
n = cut = 0
for f in sorted(p for p in src.glob(pattern) if p.is_file()):
    raw = f.read_bytes()
    text = raw.decode(errors='replace')
    for a, b in SUBS:
        text = text.replace(a, b)
    out = dst / f.name
    if len(text.encode()) > 190 * 1024:
        lines = text.splitlines()
        text = '\n'.join([*lines[:300], f'[... {len(lines) - 600} lines cut: the raw file is {len(raw):,} B, sha256 '
                          f'{hashlib.sha256(raw).hexdigest()}; the first and last 300 lines kept ...]',
                          *lines[-300:]]) + '\n'
        manifest[out.relative_to(root).as_posix()] = {'raw_bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest(),
                                                      'raw_lines': len(lines), 'kept': 'first and last 300 lines'}
        cut += 1
    out.write_text(text)
    n += 1
manifest_path.write_text(json.dumps(dict(sorted(manifest.items())), indent=1) + '\n')
print(f'{n} files filed into {dst.relative_to(root)}, {cut} excerpted')
