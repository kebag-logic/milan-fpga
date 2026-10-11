#!/usr/bin/env python3
"""R606-3: plan, stage-check and rom_words digest of linked split ELFs with a tree's ctrl_memory.py.

usage: plan_images.py <tree> <objcopy> <elf>...
Per image: ELF sha256 prefix, rom word count, sha256 of the rom words, whether
those words equal `objcopy -O binary` of the ELF (zero-padded to a word), and
the plan summary or the refusal.
"""
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

tree, objcopy = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(tree / "sw/litex"))
import ctrl_memory as cm  # noqa: E402

STAGES = {"1x1": 3344, "8x8": 13264}
for elf in map(Path, sys.argv[3:]):
    image = cm.read_elf(elf)
    stage = STAGES["8x8" if "8x8" in elf.parent.name else "1x1"]
    try:
        cm.check_stage(image, stage, elf.parent.name)
        verdict = json.dumps(cm.plan(image).summary(), sort_keys=True)
    except cm.Refusal as exc:
        verdict = f"REFUSED {exc.rule}: {exc}"
    words = cm.rom_words(image)
    packed = struct.pack(f"<{len(words)}I", *words)
    with tempfile.TemporaryDirectory() as tmp:
        binary = Path(tmp) / "image.bin"
        subprocess.run([objcopy, "-O", "binary", str(elf), str(binary)], check=True)
        loaded = binary.read_bytes()
    same = packed == loaded + bytes(-len(loaded) % 4)
    print(elf.parent.name, hashlib.sha256(elf.read_bytes()).hexdigest()[:16], len(words),
          hashlib.sha256(packed).hexdigest(), f"objcopy_equal={same}", verdict)
