"""Write every group script a tree's CPU budget harness generates for a point, from one build's build.json.

usage: python3 -I scripts_8x8.py TREE BUILD_JSON POINT OUT.json
Prints and stores each group's name and the SHA-256 of its script (scenario.all_groups, Group.script()).
"""
import hashlib
import json
import sys
from pathlib import Path

tree, build_json, label, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
sys.path.insert(0, str(tree / "tb/verilator/ctrl_service_budget"))
import scenario  # noqa: E402

build = json.loads(build_json.read_text())
p = scenario.point(label, build)
groups = scenario.all_groups(p, build)
res = {g.name: hashlib.sha256(g.script().encode()).hexdigest() for g in groups}
out.write_text(json.dumps({"tree": str(tree), "point": label, "groups": res}, indent=1, sort_keys=True) + "\n")
print(f"{label}: {len(res)} groups")
