"""Meta-run: the control that only the priority1 255 pass catches, with its
named check renamed to the shipping pass's spelling. The arm must report
that name missed, so a fourth-pass failure cannot stand in for it."""
import sys, importlib.util
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
name = "mastership sets the microcode's presence bit"
row = next(x for x in m.MUTATIONS if x[0] == name)
m.MUTATIONS = [row[:4] + ("#82 Pdelay loss: that mastership commit has gmPresent",)]
print("meta: named", m.MUTATIONS[0][4], flush=True)
sys.exit(m.main())
