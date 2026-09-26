"""Print what require_tool returns on this host for every tool name the runner looks up.

Usage: python3 -I host_lookup_probe.py <path-to-act_ci.py>
Loads the module without running main, calls only require_tool, and compares
each result with the pre-change rule Path(which(name, path=SAFE_PATH)).resolve().
"""
import importlib.util
import pathlib
import re
import shutil
import sys

source = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("act_ci_probe", source)
module = importlib.util.module_from_spec(spec)
sys.modules["act_ci_probe"] = module
spec.loader.exec_module(module)
names = sorted(set(re.findall(r'require_tool\("([^"]+)"\)', source.read_text(encoding="utf-8"))))
names = sorted(set(names) | set(module.SLOT_HOST_TOOLS))
changed = []
for name in names:
    found = shutil.which(name, path=module.SAFE_PATH)
    old = str(pathlib.Path(found).resolve()) if found else None
    try:
        new = module.require_tool(name)
    except module.Refusal as exc:
        new = f"Refusal: {exc}"
    marker = "SAME" if new == old else "DIFF"
    if marker == "DIFF":
        changed.append(name)
    print(f"{marker} {name}: new={new} old={old} basename={pathlib.Path(new).name}")
print(f"changed tools: {changed}")
sys.exit(0 if changed == ["pasta"] else 1)
