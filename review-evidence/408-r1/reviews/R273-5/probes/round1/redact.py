#!/usr/bin/env python3
"""Replace this host's local paths in receipts with neutral placeholders and
record every substitution count. Usage: redact.py <packet-dir> <pairs.json>
where pairs.json is a list of [local, placeholder] (applied in order)."""
import json
from pathlib import Path
import sys

packet = Path(sys.argv[1])
pairs = json.loads(Path(sys.argv[2]).read_text())
lines, total = [], 0
for path in sorted((packet / "receipts").rglob("*")):
    if not path.is_file() or path.name.startswith("60-report-before"):
        continue
    data = path.read_bytes()
    counts = []
    for local, placeholder in pairs:
        n = data.count(local.encode())
        if n:
            data = data.replace(local.encode(), placeholder.encode())
            counts.append(f"{placeholder}={n}")
            total += n
    if counts:
        path.write_bytes(data)
        lines.append(f"{path.relative_to(packet)}: {', '.join(counts)}")
report = packet / "receipts/95-redaction.txt"
report.write_text(
    "Local paths replaced by placeholders (nothing else changed): "
    + ", ".join(p for _l, p in pairs) + f"\n{total} substitutions\n"
    + "\n".join(lines) + "\n")
print(f"{total} substitutions in {len(lines)} files")
