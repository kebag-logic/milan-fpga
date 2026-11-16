#!/usr/bin/env python3
"""List the publishable top-level packet files; never include disposable scratch trees."""
import hashlib
from pathlib import Path

packet = Path(__file__).resolve().parent
manifest = packet / 'MANIFEST.sha256'
files = sorted(p for p in packet.iterdir() if p.is_file() and p != manifest)
manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in files))
print(f'{len(files)} publishable files; scratch excluded')
