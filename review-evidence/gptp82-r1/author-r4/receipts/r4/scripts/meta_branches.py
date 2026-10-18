"""Meta-run of the engine arm's own main() over controls that drive every
branch of the per-mutant verdict code: the pattern guard, the generator
refusal, the build failure, a survivor, both named-check narrowings (a miss
each) and both kinds of catch. Run against two revisions, the outputs must be
identical. Usage: meta_branches.py <suite_dir> <half 0|1>"""
import sys, importlib.util
from pathlib import Path
suite, half = Path(sys.argv[1]).resolve(), int(sys.argv[2])
spec = importlib.util.spec_from_file_location("mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
G, RTL = m.GENERATOR, "top/KL_gptp_engine.sv"
slew = next(x for x in m.MUTATIONS if x[0] == "slew clears at the first in-band pair")
p1 = next(x for x in m.MUTATIONS if x[0] == "mastership sets the microcode's presence bit")
rows = [
    ("meta: pattern absent", G, "no such text in the generator #82", "x", "#82 x"),
    ("meta: generator refuses", G, 'if __name__ == "__main__":\n    main()',
     'if __name__ == "__main__":\n    raise SystemExit(3)', "#82 x"),
    ("meta: RTL does not build", RTL, "endmodule : KL_gptp_engine",
     "garbage_token endmodule : KL_gptp_engine", "#82 x"),
    ("meta: comment only, survives", G, "def main() -> None:",
     "def main() -> None:  # meta", "#82 cold release: that commit's flags are gmPresent alone"),
    slew[:4] + ("slew: no such check",),
    p1[:4] + ("#82 Pdelay loss: that mastership commit has gmPresent",),
    slew,
    p1,
]
m.MUTATIONS = rows[:4] if half == 0 else rows[4:]
print("meta rows: " + "; ".join(f"{x[0]} -> {x[4]}" for x in m.MUTATIONS), flush=True)
rc = m.main()
print(f"main() rc {rc}")
sys.exit(0)
