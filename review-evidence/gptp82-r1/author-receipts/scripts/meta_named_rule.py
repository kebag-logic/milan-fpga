"""Non-vacuity of the #82 named-check rule: give one generator control an
extra name it cannot fail; the arm must report it missed and exit 1."""
import sys, importlib.util
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
sel = [x for x in m.MUTATIONS if x[0] == "becoming grandmaster keeps the departed GM"]
n, f, pat, rep, b = sel[0]
m.MUTATIONS = [(n, f, pat, rep, b + " | #82 peer wins: its commit names the peer GM")]
sys.exit(m.main())
