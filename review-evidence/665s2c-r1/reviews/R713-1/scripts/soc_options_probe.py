"""Reviewer probe: plant source mutations into the split-cache check of
sw/builder/test_soc_options.py (in memory, through its own probe) and report
which survive. usage: python3 soc_options_probe.py <checkout>"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "sw/builder"))
import test_soc_options as t  # noqa: E402

PROBES = [
    ("geometry drift: 8 KiB two-way", "CTRL_FETCH_L1 = (64, 1)", "CTRL_FETCH_L1 = (64, 2)"),
    ("geometry drift: 16 KiB", "CTRL_FETCH_L1 = (64, 1)", "CTRL_FETCH_L1 = (256, 1)"),
    ("next-line prefetch added", 'return f"--fetch-l1 --fetch-l1-sets={sets} --fetch-l1-ways={ways}"',
     'return f"--fetch-l1 --fetch-l1-sets={sets} --fetch-l1-ways={ways} --fetch-l1-hardware-prefetch=nl"'),
    ("split CPU loses the cache (control)", "                vexii_extra = \" \".join(filter(None, (vexii_extra, ctrl_cpu_args(CTRL_FETCH_L1))))",
     "                pass"),
]
with tempfile.TemporaryDirectory(prefix="r713-soc-") as tmp:
    d = Path(tmp)
    t._split_cache(d)
    print("baseline: PASS")
    for label, old, new in PROBES:
        try:
            t._split_cache(d, [(old, new)])
        except AssertionError as e:
            print(f"KILLED   {label}")
        else:
            print(f"SURVIVED {label}")
