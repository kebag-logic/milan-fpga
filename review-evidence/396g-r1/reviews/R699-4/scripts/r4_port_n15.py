#!/usr/bin/env python3
"""Port of round-2 mutant N15 (located_within never reported) to the rewritten _audio_slip.

Usage: python3 -I r4_port_n15.py <export root>
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

source = Path(sys.argv[1]) / "tb/tools/torture_campaign.py"
text = source.read_text()
old = '    if first < last:\n        event["located_within"] = [first, last]\n'
assert text.count(old) == 1, text.count(old)
with tempfile.TemporaryDirectory(prefix="r699-4-n15-") as d:
    c = Path(d) / source.name
    c.write_text(text.replace(old, "    if False:\n        pass\n"))
    r = subprocess.run([sys.executable, "-B", str(c), "--self-test"], capture_output=True, text=True, timeout=900)
print("N15-port", "KILLED" if r.returncode else "SURVIVED", "rc", r.returncode,
      sorted(set(re.findall(r"^(?:FAIL|ERROR): (\w+)", r.stderr, re.M))))
