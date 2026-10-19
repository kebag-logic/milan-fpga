"""Apply the parent's idiom scanners to the gptp-processor files a delta touches.

usage: python3 -I idiom_probe.py <parent-scripts-dir> <gptp-clone> <rev>...
Prints each rev's per-file nonzero counts and sites for every .py/.cpp/.c/.h the
delta 334e9fe6..acfef36b touches, using the parent's own scan() and sites().
"""
import importlib.util, subprocess, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

scripts, clone, revs = sys.argv[1], sys.argv[2], sys.argv[3:]
py = load(f"{scripts}/check_py_idiom.py", "check_py_idiom")
cpp = load(f"{scripts}/check_cpp_idiom.py", "check_cpp_idiom")
files = ["tb/verilator/engine/mutants.py", "tb/verilator/engine/sim_main.cpp"]
for rev in revs:
    for rel in files:
        text = subprocess.run(["git", "-C", clone, "show", f"{rev}:{rel}"],
                              capture_output=True, text=True, check=True).stdout
        lines = text.count("\n")
        if rel.endswith(".py"):
            counts, sites = py.scan(text, "gptp-processor/" + rel)
            nz = {k: v for k, v in counts.items() if v}
            print(f"{rev[:8]} {rel}: {lines} lines; py nonzero {nz}")
            for k, v in sorted(sites.items()) if isinstance(sites, dict) else []:
                for s in v:
                    print(f"  site {k}: {s}")
        else:
            counts = cpp.scan(text, "gptp-processor/" + rel)
            nz = {k: v for k, v in counts.items() if v}
            print(f"{rev[:8]} {rel}: {lines} lines; cpp nonzero {nz}")
            print(f"  long functions (start, length): {cpp.long_functions(cpp.blank_non_code(text))}")
