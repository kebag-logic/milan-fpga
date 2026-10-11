"""What ctrl_pin reads from each Makefile builder (targets, recipes, stack targets, named compilers' count), as
JSON, for comparing two checkouts. Usage: make_reading.py <checkout> <work>"""
import json
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.dont_write_bytecode = True
import ctrl_pin  # noqa: E402
from ctrl_configs import makefiles  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
link = work / "stack-link"
if not link.is_symlink():
    link.symlink_to(ctrl_pin.STACK, target_is_directory=True)
out = {}
for mk in makefiles():
    rel = mk.relative_to(ctrl_pin.ROOT).as_posix()
    defined = ctrl_pin.targets(mk, [f"STACK_DIR={link}"])
    out[rel] = {"targets": {k: sorted(v) for k, v in sorted(defined.items())},
                "recipes": {t: ctrl_pin.recipes(mk, t, [f"STACK_DIR={link}"]) for t in sorted(defined)},
                "stack_targets": ctrl_pin.stack_targets(mk, link)}
text = json.dumps(out, indent=1, sort_keys=True).replace(str(root), "<root>").replace(str(work), "<work>")
print(text)
