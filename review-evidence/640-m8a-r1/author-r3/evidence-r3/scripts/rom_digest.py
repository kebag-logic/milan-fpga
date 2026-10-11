#!/usr/bin/env python3
"""Plan and rom_words digest of each split ELF, with the tree's ctrl_memory.py."""
import hashlib
import json
import struct
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "sw/litex"))
import ctrl_memory as cm  # noqa: E402

for elf in sys.argv[2:]:
    path = Path(elf)
    image = cm.read_elf(path)
    try:
        plan = cm.plan(image)
        verdict = json.dumps(plan.summary(), sort_keys=True)
    except cm.Refusal as exc:
        verdict = f"REFUSED {exc.rule}: {exc}"
    words = cm.rom_words(image)
    digest = hashlib.sha256(struct.pack(f"<{len(words)}I", *words)).hexdigest()
    print(path.parent.name, hashlib.sha256(path.read_bytes()).hexdigest()[:16], len(words), digest, verdict)
