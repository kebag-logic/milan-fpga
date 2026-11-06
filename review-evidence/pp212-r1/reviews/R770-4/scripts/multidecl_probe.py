#!/usr/bin/env python3
"""Run the parent gate's MULTI_DECL_RE on the three round-3 lines and their
round-4 splits. Usage: multidecl_probe.py <parent-checkout>"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("cci", sys.argv[1] + "/scripts/check_cpp_idiom.py")
sys.path.insert(0, sys.argv[1] + "/scripts")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for s in ("    int e = -1, q = -1;\n", "    int e = -1;\n    int q = -1;\n",
          "  const int sinks[] = {0, 3};\n", "  const int sink_a = 0;\n  const int sink_b = 3;\n"):
    print(len(m.MULTI_DECL_RE.findall(s)), repr(s))
