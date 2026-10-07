#!/usr/bin/env python3
"""Apply the parent's C++ idiom scanner (scripts/check_cpp_idiom.py at parent dev
28f9666f, copied beside this script) to the processor bench sources of each given
tree: long functions (> LONG_FUNCTION_LINES) and the per-file idiom counts.
usage: function_length.py TREE...
"""
import importlib.util, json, sys
from pathlib import Path
here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cci", here / "parent_check_cpp_idiom_28f9666f.py")
cci = importlib.util.module_from_spec(spec); spec.loader.exec_module(cci)
out = {}
for t in sys.argv[1:]:
    tree = Path(t)
    rec = {}
    for f in sorted(list(tree.glob("tb/**/*.cpp")) + list(tree.glob("tb/**/*.hpp")) + list(tree.glob("tb/**/*.h"))):
        rel = str(f.relative_to(tree))
        if any(part.startswith("obj") for part in Path(rel).parts):
            continue
        text = f.read_text(errors="replace")
        lf = cci.long_functions(cci.blank_non_code(text))
        counts = cci.scan(text, rel)
        if lf or rel in ("tb/pp_top/sim_main.cpp", "tb/aecp_notify/sim_main.cpp"):
            rec[rel] = {"long_functions": lf, "counts": dict(counts) if hasattr(counts, "items") else str(counts)}
    out[tree.name] = {"limit": cci.LONG_FUNCTION_LINES, "files": rec,
                      "long_function_total": sum(len(v["long_functions"]) for v in rec.values())}
print(json.dumps(out, indent=1))
