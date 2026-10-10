"""List every plant of the ctrl and AECP mutation tables of a checkout: name, file, killing test(s).
usage: python3 -I mutant_tables.py <checkout>   (prints one line per plant)"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_mutants, aecp_mutants  # noqa: E402
def fields(m):
    d = m._asdict() if hasattr(m, "_asdict") else getattr(m, "__dict__", {})
    if not d and hasattr(m, "__dataclass_fields__"):
        d = {k: getattr(m, k) for k in m.__dataclass_fields__}
    return d
for table, rows in (("ctrl", ctrl_mutants.MUTANTS), ("aecp", aecp_mutants.DEFECTS)):
    for m in rows:
        d = fields(m)
        if not d and isinstance(m, tuple):
            d = {"tuple": m}
        name = d.get("name", d.get("tuple", ("?",))[0])
        f = d.get("file", d.get("path", ""))
        kill = d.get("killers", d.get("kills", d.get("test", d.get("tests", ""))))
        print(table, name, Path(str(f)).name, kill, sep="\t")
