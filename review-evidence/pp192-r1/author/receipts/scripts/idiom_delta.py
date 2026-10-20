"""usage: idiom_delta.py <parent-root> <processor-repo> <base> <head> <file...>
Score each processor C++ file at base and head with the parent's C++ idiom gate's own
`scan` (scripts/check_cpp_idiom.py) and print every count that moves."""
import importlib.util
import subprocess
import sys
from pathlib import Path

parent, repo, base, head, *files = sys.argv[1:]
spec = importlib.util.spec_from_file_location(
    "check_cpp_idiom", Path(parent) / "scripts/check_cpp_idiom.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def text(rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


moved = 0
for f in files:
    b, h = mod.scan(text(base, f), f), mod.scan(text(head, f), f)
    for key in sorted(set(b) | set(h)):
        if b.get(key, 0) != h.get(key, 0):
            moved += 1
            print(f"{f}: {key} {b.get(key, 0)} -> {h.get(key, 0)}")
    print(f"{f}: {dict(h)}")
print(f"{moved} counts move")
