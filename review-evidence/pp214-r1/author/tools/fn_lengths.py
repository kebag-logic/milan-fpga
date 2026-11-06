"""fn_lengths.py <gate.py> <file> <prefix>...: the gate's own length of every function whose first line starts with a prefix."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
text = open(sys.argv[2]).read()
lines = text.splitlines()
for n, length in gate.long_functions(gate.blank_non_code(text), 0):
    if any(lines[n - 1].strip().startswith(p) for p in sys.argv[3:]):
        print(f"{n}\t{length}\t{lines[n - 1].strip()}")
