"""Usage: python3 -I mutant_anchor_probe.py <repo>
Loads the candidate's tb/verilator/milan_dp/dynmap_mutants.py and checks that
every mutation pattern occurs exactly once in the file the arm plants into
(no build, no run)."""
import importlib.util, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
mod_path = repo / "tb/verilator/milan_dp/dynmap_mutants.py"
spec = importlib.util.spec_from_file_location("dynmap_mutants", mod_path)
m = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(mod_path.parent))
spec.loader.exec_module(m)
bad = 0
for mut in m.MUTATIONS:
    leg, name, edits = mut[:3]
    where = mut[4] if len(mut) > 4 else ""
    src = m.SHADOW_RTL if where == "shadow" else (m.PP_HDL / where[3:] if where.startswith("pp:") else m.DP_RTL)
    text = Path(src).read_text()
    for pat, _rep in edits:
        c = text.count(pat)
        if c != 1:
            bad += 1
            print(f"BAD {name!r} in {Path(src).name}: {c}")
print(f"{len(m.MUTATIONS)} mutations, {bad} pattern(s) not matching exactly once")
sys.exit(1 if bad else 0)
