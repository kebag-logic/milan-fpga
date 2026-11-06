"""cpp_scan_head.py <gate.py> <file>...: per-rule counts of the parent's C++ idiom gate on named files."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
g = importlib.util.module_from_spec(spec); sys.modules["gate"] = g; spec.loader.exec_module(g)
for f in sys.argv[2:]:
    text = open(f).read()
    print(f, dict(g.scan(text, f.split("/scratch/head/")[-1])))
