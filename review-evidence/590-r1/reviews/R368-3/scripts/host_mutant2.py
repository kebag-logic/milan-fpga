#!/usr/bin/env python3
"""Review probe R368-2: grade mutated firmware text with the unchanged host gate.

Usage: python3 -B host_mutant2.py <repo-root> <mutation-name>
Extends the round-1 probe (same edge-cross/byte-only anchors) with weaker
edge-cross variants and an ownership-ignoring copy. The repository is not
modified: the gate reads the mutated text from a temporary file through its
FIRMWARE path attribute. Exit 0 = the gate passed the mutant (SURVIVES).
"""
from pathlib import Path
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
name = sys.argv[2]
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as gate  # noqa: E402

GUARD = "if ((i & 3u) == 0 && next - i >= 4u &&"
MUTATIONS = {
    # word store may cover 1..3 bytes of the next record (round-1 F3 mutant)
    "edge-cross": (GUARD, "if ((i & 3u) == 0 && next - i >= 1u &&"),
    # crosses only when the edge residue is 2 or 3
    "edge-cross-2": (GUARD, "if ((i & 3u) == 0 && next - i >= 2u &&"),
    # crosses one byte, only when the edge residue is 3
    "edge-cross-3": (GUARD, "if ((i & 3u) == 0 && next - i >= 3u &&"),
    # the ownership vector is ignored: open records are copied too
    "ignore-ownership": ("copy = !((own[rec.id >> 5] >> (rec.id & 31u)) & 1u);",
                         "copy = 1 | (int)(own[0] & 0u);"),
    # the word path is never taken (the pre-#592 byte copy); must survive
    "byte-only": (GUARD, "if (0 && next - i >= 4u &&"),
}
old, new = MUTATIONS[name]
text = gate.FIRMWARE.read_text()
assert text.count(old) == 1, "mutation anchor is not unique"
with tempfile.TemporaryDirectory(prefix="r368-2-mut-") as tmp:
    mutated = Path(tmp) / "milan_baremetal.c"
    mutated.write_text(text.replace(old, new))
    gate.FIRMWARE = mutated
    sys.argv = [sys.argv[0]]
    rc = gate.main()
print(f"MUTANT {name}: {'SURVIVES (gate rc 0)' if rc == 0 else 'KILLED (gate rc %d)' % rc}")
sys.exit(rc)
