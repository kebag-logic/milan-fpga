#!/usr/bin/env python3
"""Replace host-identifying absolute paths in publishable receipts.

usage: sanitize_receipts.py <packet-dir> <clone-dir> [<extra-prefix>=<label> ...]
Rewrites, in place, every regular text file under <packet>/receipts and
<packet>/scripts: <clone-dir> -> <clone>, <packet-dir> -> <packet>, each
extra prefix -> its label, the user's home -> $HOME, and any per-session
scratch of the form /tmp/<name>-<uid>/ -> <tmp>/. Prints each file changed.
Symlinks are not followed; this script does not rewrite itself.
"""
import os
import re
import sys
from pathlib import Path

packet = Path(sys.argv[1]).resolve()
subs = [(str(Path(sys.argv[2]).resolve()), "<clone>"), (str(packet), "<packet>")]
subs += [tuple(arg.split("=", 1)) for arg in sys.argv[3:]]
subs.append((os.path.expanduser("~"), "$HOME"))
session_tmp = re.compile(r"/tmp/[A-Za-z]+-[0-9]+/")
me = Path(__file__).resolve()
for sub in ("receipts", "scripts"):
    for path in sorted((packet / sub).rglob("*")):
        if path.is_symlink() or not path.is_file() or path.resolve() == me:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"binary, left as is: {path.relative_to(packet)}")
            continue
        new = text
        for old, label in subs:
            new = new.replace(old, label)
        new = session_tmp.sub("<tmp>/", new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"sanitized: {path.relative_to(packet)}")
