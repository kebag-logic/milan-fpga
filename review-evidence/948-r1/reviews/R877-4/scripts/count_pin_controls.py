"""Count ctrl_pin.pin_controls' arms in a checkout without running them.

Rebuilds pin_controls with its arm-execution loop replaced by a print of the arm names, and counts the
lifecycle cases by the same replacement. Usage: python3 -I count_pin_controls.py <checkout-root>
"""
import inspect, sys, textwrap
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_pin, ctrl_pin_lifecycle  # noqa: E402

src = textwrap.dedent(inspect.getsource(ctrl_pin.pin_controls))
anchor = "    bad = 0\n    for what, spoil, check, needle in arms:"
assert src.count(anchor) == 1, "pin_controls anchor"
src = src[:src.index(anchor)] + "    return arms\n"
src = src.replace("def pin_controls(", "def pin_arms(", 1)
ns = dict(vars(ctrl_pin))
exec(compile(src, "pin_arms", "exec"), ns)

lsrc = textwrap.dedent(inspect.getsource(ctrl_pin_lifecycle.controls))
lns = dict(vars(ctrl_pin_lifecycle))
ret = lsrc.rstrip().splitlines()[-1]
assert ret.strip() == "return bad, len(cases)", ret
import ast
tree = ast.parse(lsrc)
fn = tree.body[0]
# keep statements up to the first loop over cases
body = []
for stmt in fn.body:
    if isinstance(stmt, ast.For):
        break
    body.append(stmt)
body.append(ast.parse("return cases").body[0])
fn.body = body
fn.name = "lifecycle_cases"
exec(compile(ast.fix_missing_locations(tree), "lifecycle_cases", "exec"), lns)

work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
from ctrl_configs import makefiles  # noqa: E402
arms = ns["pin_arms"](work, makefiles())
for a in arms:
    print("ARM", a[0])
clone = ctrl_pin.Clone(work / "lc", ctrl_pin.stack_gitlink())
cases = lns["lifecycle_cases"](clone)
for c in cases:
    print("LIFECYCLE", c[0] if isinstance(c, tuple) else c)
print(f"TOTAL arms={len(arms)} lifecycle={len(cases)} pin_controls={len(arms) + len(cases)}")
