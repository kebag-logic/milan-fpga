"""cpp_scan.py <gate.py> <file>...: every count of the gate's scan() for each file, and the longest function."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
for f in sys.argv[2:]:
    text = open(f).read()
    c = gate.scan(text, f)
    lf = gate.long_functions(gate.blank_non_code(text), 0)
    print(f, {k: v for k, v in c.items()}, "longest", max(lf, key=lambda x: x[1]) if lf else None)
