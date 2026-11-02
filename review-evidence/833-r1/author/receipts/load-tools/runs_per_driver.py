# Scratch only: counts owner.run calls and census passes in one real `normal(detect)` driver run, in the given tree, and its wall time.
import os, sys, tempfile, time
from pathlib import Path
tree = Path(sys.argv[1]); os.chdir(tree)
sys.path.insert(0, str(tree / "scripts")); sys.path.insert(0, str(tree / "tb/verilator/gptp_shadow"))
os.environ.update(PYTHONDONTWRITEBYTECODE="1")
import test_mutant_lifecycle as l
from pathlib import Path as P
trace = """
import atexit, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
"""
with tempfile.TemporaryDirectory() as d:
    d = P(d).resolve()
    root, probe = l.fixture(d, "detect")
    probe.env["PROBE_MODE"] = "detect"
    # count at the production boundary, in the fixture's own copy of the owner
    owned = root / "scripts/owned_process.py"
    text = owned.read_text()
    assert "    def _descendants(self)" in text
    text = text.replace("    def _descendants(self) -> dict[int, tuple[int, str]]:\n",
        "    def _descendants(self) -> dict[int, tuple[int, str]]:\n        open(os.environ['COUNTS'], 'a').write('c')\n")
    text = text.replace('        self.checkpoint()\n        self.root_notified = False\n',
        "        self.checkpoint()\n        open(os.environ['COUNTS'], 'a').write('r')\n        self.root_notified = False\n")
    owned.write_text(text)
    l.commit(root)
    counts = d / "counts"; probe.env["COUNTS"] = str(counts)
    start = time.monotonic()
    probe.start([sys.executable, str(root / l.DRIVER)])
    status = probe.process.wait(timeout=300)
    took = time.monotonic() - start
    c = counts.read_text()
    print(dict(tree=tree.name, rc=status, seconds=round(took, 1), owner_runs=c.count("r"), census_passes=c.count("c")))
