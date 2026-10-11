"""R584-9: every call of `run` in the modules that import it from ctrl_build, checked against the old signature
run(argv, cwd=None): any call with a third positional argument or a keyword other than cwd is listed.
Usage: python3 -I run_alias_calls.py <checkout>. Writes nothing."""
import ast
import sys
from pathlib import Path

test = Path(sys.argv[1]).resolve() / "sw/firmware/ctrl/test"
for name in ("ctrl_runs.py", "ctrl_srp_image.py", "ctrl_arms.py", "srp_arms.py", "aecp_arms.py"):
    tree = ast.parse((test / name).read_text(encoding="utf-8"))
    beyond = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
              and n.func.id == "run" and (len(n.args) > 2 or any(k.arg != "cwd" for k in n.keywords))]
    own = any(isinstance(n, ast.FunctionDef) and n.name == "run" for n in tree.body)
    print(f"{name}: calls of run beyond (argv, cwd): {beyond}; defines its own run: {own}")
