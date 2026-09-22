#!/usr/bin/env python3
"""R239: independently verify the pinned Verilator 5.050 tool identity.

Reads the pacman local-db mtree of verilator-5.050-1 inside the on-disk image
layer the scoped selector points at, and hashes every regular file it lists
(sha256) against the layer's bytes.  Read-only; installs nothing, starts no
container.  Prints one line per mismatch/absence and a summary.
"""
import gzip
import hashlib
import re
import sys
from pathlib import Path

LAYER = Path(sys.argv[1])
pkg = LAYER / "var/lib/pacman/local/verilator-5.050-1"
raw = (pkg / "mtree").read_bytes()
text = gzip.decompress(raw).decode()

defaults = {}
ok = absent = bad = other = 0
absent_list, bad_list = [], []
for line in text.splitlines():
    if not line or line.startswith("#"):
        continue
    if line.startswith("/set "):
        for kv in line.split()[1:]:
            k, _, v = kv.partition("=")
            defaults[k] = v
        continue
    parts = line.split()
    path = parts[0]
    attrs = dict(defaults)
    for kv in parts[1:]:
        k, _, v = kv.partition("=")
        attrs[k] = v
    if attrs.get("type") != "file" or path.startswith("./."):
        other += 1
        continue
    # mtree escapes: \040 etc.
    rel = re.sub(r"\\([0-7]{3})", lambda m: chr(int(m.group(1), 8)), path[2:])
    f = LAYER / rel
    if not f.is_file():
        absent += 1
        absent_list.append(rel)
        continue
    digest = hashlib.sha256(f.read_bytes()).hexdigest()
    if digest == attrs.get("sha256digest"):
        ok += 1
    else:
        bad += 1
        bad_list.append(rel)

for rel in absent_list:
    print(f"ABSENT  {rel}")
for rel in bad_list:
    print(f"MISMATCH {rel}")
print(f"mtree regular files: match={ok} absent={absent} mismatch={bad} (non-file entries skipped={other})")
vb = LAYER / "usr/bin/verilator_bin"
for cand in (LAYER / "usr/bin/verilator", LAYER / "usr/bin/verilator_bin",
             LAYER / "usr/share/verilator/bin/verilator_bin"):
    if cand.exists():
        print(f"sha256 {hashlib.sha256(cand.read_bytes()).hexdigest()}  {cand.relative_to(LAYER)}"
              f"{' -> ' + str(cand.resolve().relative_to(LAYER.resolve())) if cand.is_symlink() else ''}")
sys.exit(0 if bad == 0 else 1)
