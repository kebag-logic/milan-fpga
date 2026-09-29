import importlib.util, sys, tempfile
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec); sys.argv = [str(suite / "mutants.py")]; spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(prefix="mfcause-", dir="$VALIDATION_STORAGE/617-a434-work/tmp") as td:
    ok, lines = m.makeflags_result(Path(td)); print("\n".join(lines))
