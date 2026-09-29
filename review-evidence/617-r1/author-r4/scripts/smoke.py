import importlib.util, sys, tempfile
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec); sys.argv = [str(suite / "mutants.py")]; spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(dir="$VALIDATION_STORAGE/617-a434-work/tmp") as td:
    w = Path(td)
    for ok, lines in [m.makeflags_result(w), m.build_break_result(w)]:
        print(ok); print("\n".join(lines))
    leg, name, edits, breaks = [x for x in m.MUTATIONS if x[1].startswith("RM9")][0]
    ok, lines = m.mutant_result(leg, w, name, edits, breaks); print(ok); print("\n".join(lines))
