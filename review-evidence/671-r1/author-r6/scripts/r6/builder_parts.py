"""Run consecutive parts of the builder bank within a foreground time limit.

Usage: builder_parts.py TREE PART PARTS [builder options]
The test order and functions come from the bank's own main loop. Each part
runs its assigned functions unchanged, including the required-elaboration
verdict. Collect every part before claiming the complete bank.
"""
import ast
import runpy
import sys
from pathlib import Path

tree, part, parts = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
source = tree / "sw/builder/test_builder.py"
sys.path.insert(0, str(source.parent))
sys.argv = [str(source), *sys.argv[4:]]
namespace = runpy.run_path(str(source), run_name="builder_part")
syntax = ast.parse(source.read_text())
main = syntax.body[-1]
assert isinstance(main, ast.If)
for statement in main.body:
    if isinstance(statement, (ast.Import, ast.ImportFrom)):
        exec(compile(ast.Module(body=[statement], type_ignores=[]), str(source), "exec"), namespace)
loop = next(statement for statement in main.body if isinstance(statement, ast.For))
names = [item.id for item in loop.iter.elts]
lo, hi = len(names) * part // parts, len(names) * (part + 1) // parts
assert 0 <= part < parts and lo < hi
print(f"BUILDER PART {part + 1}/{parts}: functions {lo + 1} through {hi} of {len(names)}", flush=True)
for name in names[lo:hi]:
    print(f"{name}:", flush=True)
    namespace[name]()
for gate, why, _kind in namespace["SKIPPED"]:
    print(f"NOT RUN [{gate}]: {why}", flush=True)
rc = namespace["_require_elaboration_verdict"](namespace["SKIPPED"]) if "--require-elaboration" in sys.argv else 0
print(f"BUILDER PART {part + 1}/{parts}: rc={rc}, {len(namespace['SKIPPED'])} skipped arm(s)", flush=True)
raise SystemExit(rc)
