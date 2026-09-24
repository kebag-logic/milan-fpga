#!/usr/bin/env python3
"""[A261] scratch: copy the small text receipts of the final run into the
output directory, redacting the home directory and scratch prefixes. Files
over 400 KiB (closure-extend JSONL, audits) stay in scratch and are listed."""
import hashlib
import re
import sys
from pathlib import Path

src = Path("$VALIDATION_STORAGE/408-a261/final")
dst = Path(sys.argv[1])
extra = [Path("$VALIDATION_STORAGE/408-a261/utf8")]
LIMIT = 400 * 1024
redact = [(re.compile(re.escape(str(Path.home()))), "$HOME"),
          (re.compile(r"$VALIDATION_STORAGE/408-a261"), "$SCRATCH"),
          (re.compile(r"$LANES/408-409-boot-gate-retire"), "$LANE"),
          (re.compile(r"$VALIDATION_TOOLS"), "$TOOLS")]
kept, left = [], []
for root in [src] + extra:
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root.parent if root in extra else root)
        if path.stat().st_size > LIMIT or path.suffix in (".c",) and root is src:
            left.append((str(rel), path.stat().st_size))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            left.append((str(rel), path.stat().st_size))
            continue
        for pattern, name in redact:
            text = pattern.sub(name, text)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        kept.append((str(rel), hashlib.sha256(text.encode()).hexdigest()))
(dst / "MANIFEST.sha256").write_text(
    "".join(f"{digest}  {rel}\n" for rel, digest in kept), encoding="utf-8")
(dst / "LEFT-IN-SCRATCH.txt").write_text(
    "".join(f"{size:>10}  {rel}\n" for rel, size in left), encoding="utf-8")
print(f"copied {len(kept)} file(s); {len(left)} left in scratch")
