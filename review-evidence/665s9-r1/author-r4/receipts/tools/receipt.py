#!/usr/bin/env python3
"""receipt.py <src-log> <dest> <head> <command words...> - a gate's receipt: its head and command, then the log with
host paths replaced by placeholders, or (over 200 KB) its size, sha256 and the lines naming a verdict."""
import hashlib, re, sys
from pathlib import Path
src, dest, head, command = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], " ".join(sys.argv[4:])
raw = src.read_bytes()
text = raw.decode(errors="replace")
for path, mark in (("<scratch>", "<scratch>"), ("<lane>", "<lane>"),
                   ("<tools>", "<tools>"), ("<data>", "<data>"), ("<home>", "<home>"),
                   ("<scratch>/tmpci", "<tmp>"), ("<scratch>/tmp", "<tmp>")):
    text = text.replace(path, mark)
head_line = f"head {head}\ncommand: {command}\nfull log: {len(raw)} bytes, sha256 {hashlib.sha256(raw).hexdigest()}\n"
if len(text.encode()) > 200_000:
    keep = [l for l in text.splitlines() if re.search(r"rc=|PASS|FAIL|caught|ESCAPED|REFUSED|finding|checks:|error|Error", l)]
    text = "--- over 200 KB: the verdict lines only\n" + "\n".join(keep[-400:]) + "\n"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(head_line + "---\n" + text)
print(dest.name, len(dest.read_bytes()))
