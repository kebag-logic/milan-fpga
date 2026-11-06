"""cpp_sites.py <gate.py> <file>...: the line and snippet of every multi-declarator and long-function finding."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
for f in sys.argv[2:]:
    text = open(f).read()
    for key in ("multi-declarator declaration", "long function"):
        for n, s in gate.sites(text, key, f):
            print(f"{f}:{n}: [{key}] {s}")
