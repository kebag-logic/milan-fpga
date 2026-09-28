#!/usr/bin/env python3
"""Review probe: grade a mutated firmware text with the unchanged host gate.

Usage: python3 -B host_mutant.py <repo-root> <mutation-name>
The repository is not modified: the gate reads the mutated text from a
temporary file through its FIRMWARE path attribute. Exit 0 = the gate passed
the mutant (mutant SURVIVES); exit 1 = the gate reported findings (killed).
"""
from pathlib import Path
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
name = sys.argv[2]
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as gate  # noqa: E402

MUTATIONS = {
    # word store may cover up to three bytes past the record edge
    "edge-cross": ("if ((i & 3u) == 0 && next - i >= 4u &&",
                   "if ((i & 3u) == 0 && next - i >= 1u &&"),
    # the word path is never taken (the pre-#592 byte copy)
    "byte-only": ("if ((i & 3u) == 0 && next - i >= 4u &&",
                  "if (0 && next - i >= 4u &&"),
}
old, new = MUTATIONS[name]
text = gate.FIRMWARE.read_text()
assert text.count(old) == 1, "mutation anchor is not unique"
with tempfile.TemporaryDirectory(prefix="r368-mut-") as tmp:
    mutated = Path(tmp) / "milan_baremetal.c"
    mutated.write_text(text.replace(old, new))
    gate.FIRMWARE = mutated
    sys.argv = [sys.argv[0]]
    rc = gate.main()
print(f"MUTANT {name}: {'SURVIVES (gate rc 0)' if rc == 0 else 'KILLED (gate rc %d)' % rc}")
sys.exit(rc)
