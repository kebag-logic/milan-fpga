"""[R383] Count the builder bank's registered arms (the tuple the __main__
loop iterates in sw/builder/test_builder.py) and check that each one printed
its `<name>:` header in a bank log, and that the #607 arm printed the four
shipping PASS markers.  Usage: arm_census.py <tree> <bank log>"""
import ast, re, sys
from pathlib import Path
tree, log = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
mod = ast.parse((tree / "sw/builder/test_builder.py").read_text())
main = [n for n in mod.body if isinstance(n, ast.If) and "__main__" in ast.unparse(n.test)][-1]
loops = [n for n in ast.walk(main) if isinstance(n, ast.For) and isinstance(n.iter, ast.Tuple)]
names = [e.id for e in loops[0].iter.elts]
print("registered arms:", len(names), "unique:", len(set(names)))
lines = log.splitlines()
missing = [n for n in names if f"{n}:" not in lines]
print("arms without a header line in the log:", missing or "none")
order = [lines.index(f"{n}:") for n in names if f"{n}:" in lines]
print("headers in registration order:", order == sorted(order))
print("607 arm position:", names.index("test_clock_crossing_constraints") + 1)
ship = [l for l in lines if re.match(r"\[constraints\] shipping .* PASS$", l)]
print("shipping PASS markers:", len(ship))
for l in ship: print("  ", l[:90], "...")
print("verdict lines:", [l for l in lines if l.startswith(("ALL GATES", "--require-elaboration"))][:2])
