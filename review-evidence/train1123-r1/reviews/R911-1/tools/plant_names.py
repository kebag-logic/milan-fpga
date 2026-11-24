"""Print the defect names of the conflicted plant tables of one extracted tree, as JSON.

usage: python3 -I plant_names.py <tree-root>
The tables: aecp_mutants.DEFECTS, srp_mutants.DEFECTS, sink_mutants.mutants(), and the
8x8/1if and 1x1 one-interface SRP campaign filters' prefixes from test_ctrl_firmware.py.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
test = root / "sw/firmware/ctrl/test"
sys.path.insert(0, str(test))
out = {}
import aecp_mutants  # noqa: E402
out["aecp"] = sorted(d.name for d in aecp_mutants.DEFECTS)
import srp_mutants  # noqa: E402
out["srp"] = sorted(d.name for d in srp_mutants.DEFECTS)
try:
    import sink_mutants  # noqa: E402

    class M:
        def __init__(self, name, *a, **k):
            self.name = name
    out["sink"] = sorted(m.name for m in sink_mutants.mutants(M))
except Exception as e:  # a tree before the sink table
    out["sink"] = f"unavailable: {e!r}"
text = (test / "test_ctrl_firmware.py").read_text()
body = text[text.find("def run_srp_mutants"):]
body = body[:body.find("\ndef ", 10)]
out["srp_filters"] = re.findall(r"startswith\(\((.*?)\)\)\)", body, re.S)
print(json.dumps(out))
