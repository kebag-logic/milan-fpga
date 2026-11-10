"""Every group's script at a point, from one tree's scenario.py, as JSON {group: sha256}. usage: TREE BUILD_JSON"""
import hashlib, json, sys
from pathlib import Path
tree, build_json = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import scenario
spec = json.loads(build_json.read_text())
p = scenario.point(spec['shape'].split('_')[-1] if False else 'x', spec)
print(json.dumps({g.name: hashlib.sha256(g.script().encode()).hexdigest() for g in scenario.all_groups(p, spec)}, sort_keys=True))
