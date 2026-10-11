"""Normalise round 6's text receipts in place and index them.

Usage: collect_receipts.py REPO SCRATCH OUTPUT [EXTRA-LOG...]
Every file in OUTPUT (but MANIFEST.md) and every EXTRA-LOG is read, its
original size and SHA-256 recorded, and its text stored in OUTPUT with local
paths, the scratch and tool roots, the home directory and PATH lists
replaced by labels. A file over 190,000 bytes is hashed, not stored.
"""
import hashlib
import re
import sys
from pathlib import Path

repo, scratch, output = (Path(x).resolve() for x in sys.argv[1:4])
extra = [Path(x).resolve() for x in sys.argv[4:]]


def public_text(text: str) -> str:
    """The text with local paths replaced by labels."""
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    text = re.sub(r"PATH=\S+", "PATH=<suite-tools>", text)
    for source, label in ((str(repo), "<repo>"), (str(scratch), "<scratch>"),
                          (str(scratch.parent), "<scratch-root>"), ("$VALIDATION_TOOLS", "<tools>"),
                          (str(Path.home()), "<home>")):
        text = text.replace(source, label)
    return text


rows = ["# Round 6 receipt manifest", "",
        "Original byte sizes and SHA-256 hashes. Stored receipts have local paths and PATH lists normalized.", "",
        "| Receipt | Original bytes | Original SHA-256 | Stored |", "|---|---:|---|---|"]
sources = [(p.name, p) for p in sorted(output.iterdir()) if p.is_file() and p.name != "MANIFEST.md"]
sources += [(e.relative_to(scratch).as_posix().replace("/", "__"), e) for e in extra]
for name, path in sources:
    raw = path.read_bytes()
    if len(raw) <= 190_000:
        (output / name).write_text(public_text(raw.decode(errors="replace")))
        stored = "yes"
    else:
        (output / name).unlink(missing_ok=True)
        stored = "hash and size only"
    rows.append(f"| `{name}` | {len(raw)} | `{hashlib.sha256(raw).hexdigest()}` | {stored} |")
(output / "MANIFEST.md").write_text("\n".join(rows) + "\n")
print(f"indexed {len(sources)} receipt(s)")
