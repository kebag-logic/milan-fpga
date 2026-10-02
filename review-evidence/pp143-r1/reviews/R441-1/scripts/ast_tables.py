#!/usr/bin/env python3
"""Compare every module-level constant and every mutation function of the eight
drivers between two commits by abstract syntax tree (ast.dump, no positions).

usage: ast_tables.py REPO BASE HEAD
"""
import ast
import subprocess
import sys

DRIVERS = ["tb/acmp_talker/retry_mutants.py", "tb/adp_engine/mutants.py", "tb/maap/mutants.py",
           "tb/pp_top/aecp_dispatch_mutants.py", "tb/pp_top/aecp_mutants.py",
           "tb/pp_top/gsi_mutants.py", "tb/srp_admission/mutants.py", "tb/srp_top/mutants.py"]
#: functions that hold mutation tables or the edit/plant/judge logic
FUNCS = {"mutations", "plant", "judge", "run", "run_suite", "build_tree", "run_case", "tally",
         "completed", "failures_of"}


def items(repo: str, rev: str, path: str) -> dict[str, str]:
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True,
                         text=True, check=True).stdout
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out["const " + t.id] = ast.dump(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out["const " + node.target.id] = ast.dump(node.value) if node.value else ""
        elif isinstance(node, ast.FunctionDef) and node.name in FUNCS:
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                body = body[1:]  # docstring wording is not behaviour
            out["func " + node.name] = ast.dump(ast.Module(body=body, type_ignores=[]))
    return out


def main() -> int:
    repo, base, head = sys.argv[1:4]
    bad = 0
    for path in DRIVERS:
        a, b = items(repo, base, path), items(repo, head, path)
        for key in sorted(set(a) | set(b)):
            state = ("same" if a.get(key) == b.get(key) else
                     "ADDED" if key not in a else "REMOVED" if key not in b else "CHANGED")
            if state != "same":
                bad += key.startswith("const ") and state != "ADDED"
            print(f"{path} {key}: {state}")
    print(f"changed-or-removed constants: {bad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
