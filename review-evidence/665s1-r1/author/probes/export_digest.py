"""One digest per LiteX export directory, over compare_same.py's normalisations.

Usage: export_digest.py <export-dir>...
Each file contributes (relative path, sha256 of its normalised bytes): stamp lines
dropped; an ar archive as its members' names and bytes; a .v file's hierarchy-tree
lines, last-child glyph folded, sorted after its other lines. litex.log, a record of
the run and not a build input or output, is left out (compare_same.py grades it).
The digest is sha256 over those pairs in path order; it prints the digest, the file
count and the raw (unnormalised) digest of each directory.
"""
import hashlib
import re
import sys
from pathlib import Path

STAMP = re.compile(rb"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}")
BOX = ("│", "├", "└")


def normalised(path: Path) -> bytes:
    """The bytes compare_same.py's normalisations leave of one file."""
    data = path.read_bytes()
    if data.startswith(b"!<arch>\n"):
        out, pos = [], 8
        while pos + 60 <= len(data):
            hdr = data[pos:pos + 60]
            size = int(hdr[48:58].strip())
            out.append(hdr[0:16] + data[pos + 60:pos + 60 + size])
            pos += 60 + size + (size & 1)
        return b"\0".join(out)
    lines = [ln for ln in data.split(b"\n") if not STAMP.search(ln)]
    if path.suffix == ".v":
        tree = sorted(ln.replace("└".encode(), "├".encode()) for ln in lines
                      if ln.decode("utf-8", errors="replace").lstrip().startswith(BOX))
        lines = [ln for ln in lines if not ln.decode("utf-8", errors="replace").lstrip().startswith(BOX)] + tree
    return b"\n".join(lines)


for top in map(Path, sys.argv[1:]):
    files = sorted(p for p in top.rglob("*") if p.is_file() and p.name != "litex.log")
    norm, raw = hashlib.sha256(), hashlib.sha256()
    for p in files:
        rel = str(p.relative_to(top)).encode()
        norm.update(rel + b"\0" + hashlib.sha256(normalised(p)).digest())
        raw.update(rel + b"\0" + hashlib.sha256(p.read_bytes()).digest())
    print(f"{top.name}: normalised {norm.hexdigest()} over {len(files)} files; raw {raw.hexdigest()}")
