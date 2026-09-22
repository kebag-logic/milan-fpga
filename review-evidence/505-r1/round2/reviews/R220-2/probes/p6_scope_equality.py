"""P6: what executable content changed between revisions of ci_events.py.

Top-level functions are compared by AST with docstrings removed (comments
are not in the AST); every module-level non-callable name is compared by
value after import. Reported for BASE->HEAD and R1->HEAD. Also records the
blob ids of every file the four carriers' contract checks and the AC5
measurement path read (workflows, policy page, ci_events.py, act_ci.py).
"""
from __future__ import annotations

import ast
import json
import sys
import types

from common import BASE, HEAD, R1, SCRATCH_AC5, git, load_module, show


def strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return tree


def top_level(rev: str) -> dict[str, str]:
    tree = strip_docstrings(ast.parse(show(rev, "scripts/ci_events.py")))
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[f"def {node.name}"] = ast.dump(node, include_attributes=False)
    return out


def _stable(value):
    """repr without memory addresses: a function inside a constant (GATE_STEPS
    holds predicate functions) is rendered by name; the functions themselves
    are compared by AST above."""
    if isinstance(value, types.FunctionType):
        return f"<function {value.__name__}>"
    if isinstance(value, dict):
        return "{" + ", ".join(f"{_stable(k)}: {_stable(v)}" for k, v in value.items()) + "}"
    if isinstance(value, (list, tuple)):
        inner = ", ".join(_stable(v) for v in value)
        return f"[{inner}]" if isinstance(value, list) else f"({inner})"
    if isinstance(value, (set, frozenset)):
        return "{" + ", ".join(sorted(_stable(v) for v in value)) + "}"
    return repr(value)


def constants(mod) -> dict[str, str]:
    out = {}
    for name, value in vars(mod).items():
        if name.startswith("__") or isinstance(value, (types.FunctionType, types.ModuleType, type)):
            continue
        try:
            out[name] = _stable(value)
        except Exception as exc:  # noqa: BLE001
            out[name] = f"<unrepr {exc!r}>"
    return out


def compare(a: str, b: str) -> dict:
    fa, fb = top_level(a), top_level(b)
    ma, mb = load_module(a, f"m_{a[:8]}_p6"), load_module(b, f"m_{b[:8]}_p6")
    ca, cb = constants(ma), constants(mb)
    return {
        "functions_added": sorted(set(fb) - set(fa)),
        "functions_removed": sorted(set(fa) - set(fb)),
        "functions_changed": sorted(n for n in set(fa) & set(fb) if fa[n] != fb[n]),
        "functions_unchanged_count": sum(1 for n in set(fa) & set(fb) if fa[n] == fb[n]),
        "constants_added": sorted(set(cb) - set(ca)),
        "constants_removed": sorted(set(ca) - set(cb)),
        "constants_changed": sorted(n for n in set(ca) & set(cb) if ca[n] != cb[n]),
        "constants_unchanged_count": sum(1 for n in set(ca) & set(cb) if ca[n] == cb[n]),
    }


def blobs(rev: str) -> dict[str, str]:
    paths = [".github/workflows/docs.yml", ".github/workflows/elaborate.yml",
             ".github/workflows/rtl.yml", ".github/workflows/rtl-fast.yml",
             "docs/testing/CI_WORKFLOWS.md", "scripts/ci_events.py", "scripts/act_ci.py"]
    out = {}
    for p in paths:
        out[p] = git("rev-parse", f"{rev}:{p}").strip()
    return out


def main() -> int:
    rep = {"base_to_head": compare(BASE, HEAD), "r1_to_head": compare(R1, HEAD)}
    rep["blobs"] = {rev[:8]: blobs(rev) for rev in (BASE, R1, HEAD)}
    try:
        rep["blobs"][SCRATCH_AC5[:8]] = blobs(SCRATCH_AC5)
    except Exception as exc:  # noqa: BLE001
        rep["blobs"][SCRATCH_AC5[:8]] = f"unavailable locally: {exc}"
    # Changed paths between each pair (whole tree).
    rep["paths_changed_r1_to_head"] = git("diff", "--name-only", R1, HEAD).split()
    rep["paths_changed_base_to_head"] = git("diff", "--name-only", BASE, HEAD).split()
    json.dump(rep, open(sys.argv[1], "w"), indent=1)
    print(json.dumps(rep, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
