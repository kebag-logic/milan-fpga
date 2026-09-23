#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe: are the two new annotations true?
#
# Usage: annotation_check.sh PP_BASE_CHECKOUT PP_HEAD_CHECKOUT MYPY
#   MYPY  a mypy executable (a disposable venv is enough)
#
# 1. AST audit: every `return` in main() carries an int literal, and the test
#    method has no `return <value>`.
# 2. Runtime: main() under stub tools returns an object whose type is int.
# 3. mypy over tb/pp_top/*.py at BASE and HEAD (default mode, then --strict):
#    at HEAD the two functions are annotated, so mypy now checks their bodies.
set -uo pipefail
base=$(cd "$1" && pwd)
head=$(cd "$2" && pwd)
mypy=$(cd "$(dirname "$3")" && pwd)/$(basename "$3")

python3 - "$head" <<'PYEOF'
import ast, sys
from pathlib import Path
head = Path(sys.argv[1])
for rel, fn in (("tb/pp_top/fixture_guards.py", "main"),
                ("tb/pp_top/test_fixture_guards.py", "test_compiler_environment_and_arguments")):
    tree = ast.parse((head / rel).read_text())
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == fn)
    rets = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
    print(f"{rel}::{fn} annotated -> {ast.unparse(node.returns)}; returns: "
          + (", ".join(ast.unparse(r.value) if r.value is not None else "<bare>" for r in rets) or "none"))
    if fn == "main":
        ok = rets and all(isinstance(r.value, ast.Constant) and type(r.value.value) is int for r in rets)
    else:
        ok = all(r.value is None for r in rets)
    print(f"  AST audit: {'OK' if ok else 'MISMATCH'}")
PYEOF

python3 - "$head" <<'PYEOF'
import os, subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(sys.argv[1]) / "tb/pp_top"))
import fixture_guards
done = subprocess.CompletedProcess([], 0, "")
bad = subprocess.CompletedProcess([], 1, "")
for label, results, want in (("all-pass", None, 0), ("mismatch", [done, done, done, done, done], 1)):
    if results is None:
        w = "SRP VID fixture must differ from product default 2 in the 16-bit wire value"
        c = "SRP VID fixture must differ from product default 2 in the 12-bit class-D value"
        e = lambda ms: subprocess.CompletedProcess([], 1, "".join(f"x: error: static assertion failed: {m}\n" for m in ms))
        results = [done, done, done, e([w, c]), e([c])]
    with patch("sys.argv", ["fixture_guards.py", "--", "x.sv"]), \
         patch.object(fixture_guards.subprocess, "check_output", return_value="/r\n"), \
         patch.object(fixture_guards.subprocess, "run", side_effect=results), \
         open(os.devnull, "w") as sink, patch("sys.stdout", sink):
        got = fixture_guards.main()
    print(f"runtime {label}: main() returned {got!r} of type {type(got).__name__}: "
          f"{'OK' if type(got) is int and got == want else 'MISMATCH'}")
PYEOF

for rev in base head; do
    dir=$base; [ "$rev" = head ] && dir=$head
    for mode in default strict; do
        flag=""; [ "$mode" = strict ] && flag="--strict"
        echo "== mypy $mode at $rev ($(git -C "$dir" rev-parse --short=12 HEAD))"
        (cd "$dir/tb/pp_top" && "$mypy" $flag --no-incremental --cache-dir=/dev/null \
            fixture_guards.py test_fixture_guards.py 2>&1)
        echo "mypy exit=$?"
    done
done
