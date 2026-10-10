#!/usr/bin/env python3
"""Lane B14: mask the reference peer's and the grandmaster's identifiers in packet files.

usage: redact_b14.py <packet_dir> <private_dir> <file> [<file> ...]
Each named file that holds a masked token is copied unmodified to <private_dir> (outside the
packet), then rewritten in place with the token replaced by its label. redaction.json in the
packet records each file's original and retained SHA-256 and the labels applied. The tokens come
from the environment (B14_MASK: comma-separated token=label pairs), so this file names none.
"""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

pk, priv = Path(sys.argv[1]), Path(sys.argv[2])
pairs = [p.split("=", 1) for p in os.environ["B14_MASK"].split(",") if p]
ledger_path = pk / "redaction.json"
ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
for name in sys.argv[3:]:
    f = pk / name
    data = f.read_bytes()
    text = data.decode("utf-8", errors="surrogateescape")
    labels = []
    for tok, lab in pairs:
        for variant in {tok, tok.upper()}:
            if variant in text:
                text = text.replace(variant, lab)
                labels.append(lab)
    if not labels:
        continue
    dst = priv / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, dst)
    new = text.encode("utf-8", errors="surrogateescape")
    f.write_bytes(new)
    ledger[name] = dict(original_sha256=hashlib.sha256(data).hexdigest(),
                        retained_sha256=hashlib.sha256(new).hexdigest(), labels=sorted(set(labels)))
ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: v["labels"] for k, v in ledger.items()}))
