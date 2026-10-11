"""Stage the lane's RTL with one named mutant of the parser arm applied.
Usage: stage_mutant.py <lane> <mutant-name-substring> <out-hdl-dir>"""
import importlib.util, shutil, sys
from pathlib import Path
lane, key, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
spec = importlib.util.spec_from_file_location(
    "mutants", lane / "tb/verilator/parser/mutants.py")
sys.dont_write_bytecode = True
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
(name, edits, breaks), = [x for x in m.MUTATIONS if key in x[0]]
for rel in m.RTL_SOURCES:
    (out / rel).parent.mkdir(parents=True, exist_ok=True)
    text = (lane / "hdl" / rel).read_text()
    if rel == m.PARSER:
        for a, b in edits:
            assert text.count(a) == 1, a
            text = text.replace(a, b)
    (out / rel).write_text(text)
print(name); print("\n".join(breaks))
