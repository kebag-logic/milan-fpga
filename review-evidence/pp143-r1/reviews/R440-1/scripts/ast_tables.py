#!/usr/bin/env python3
"""Compare every module-level constant and gsi's mutations() of the eight drivers at two commits."""
import ast
import subprocess
import sys

DRIVERS = ["tb/acmp_talker/retry_mutants.py", "tb/adp_engine/mutants.py", "tb/maap/mutants.py",
           "tb/pp_top/aecp_dispatch_mutants.py", "tb/pp_top/aecp_mutants.py",
           "tb/pp_top/gsi_mutants.py", "tb/srp_admission/mutants.py", "tb/srp_top/mutants.py"]


def tables(src: str) -> dict[str, str]:
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for t in targets:
                if isinstance(t, ast.Name):
                    out[t.id] = ast.dump(node.value)
        elif isinstance(node, ast.FunctionDef) and node.name == "mutations":
            out["def mutations"] = ast.dump(node)
    return out


def show(rev: str, path: str) -> str:
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True,
                          check=True).stdout


def main() -> int:
    base, head = sys.argv[1], sys.argv[2]
    bad = 0
    for path in DRIVERS:
        a, b = tables(show(base, path)), tables(show(head, path))
        same = sorted(k for k in a if k in b and a[k] == b[k])
        changed = sorted(k for k in a if k in b and a[k] != b[k])
        gone = sorted(set(a) - set(b))
        new = sorted(set(b) - set(a))
        bad += bool(changed or gone)
        print(f"{path}: same={same} changed={changed} removed={gone} added={new}")
    print("RESULT", "FAIL" if bad else "OK: no constant changed or removed")
    return bad

if __name__ == '__main__':
    sys.exit(main())
