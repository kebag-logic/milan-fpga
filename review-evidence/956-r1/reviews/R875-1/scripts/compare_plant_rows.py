"""Compare srp_talker_mutants.defects() rows between two copies (reviewer receipt)."""
import importlib.util, sys
def rows(path):
    spec = importlib.util.spec_from_file_location("m", path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.defects(lambda *a, **k: (a, tuple(sorted(k.items()))))
a, b = rows(sys.argv[1]), rows(sys.argv[2])
print("code-head rows", len(a), "head rows", len(b), "same multiset", sorted(map(repr, a)) == sorted(map(repr, b)),
      "same order", a == b)
