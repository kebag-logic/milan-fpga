import importlib.util, sys, tempfile
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec); sys.argv = [str(suite / "mutants.py")]; spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(dir="$VALIDATION_STORAGE/617-a434-work/tmp") as td:
    for i in (1, 2):
        ok, lines = m.rom_images_result(Path(td) / str(i) if False else Path(td)); print(i, ok, lines, repr(m.build_log(Path(td), "rom_images").read_text()[:200]))
