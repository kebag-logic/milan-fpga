"""Compare each group's script at this checkout with the script round 2 recorded."""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import scenario
runs = Path(sys.argv[2])
for label, point, dirs in (('A1', '1x1', ['A1', 'A1-bl']), ('A8', '8x8', ['A8', 'A8-bl']), ('B1', '1x1', ['B1', 'B1-bl']),
                           ('B8', '8x8', ['B8', 'B8-bl']), ('S1', '1x1', ['S1']), ('S8', '8x8', ['S8']),
                           ('C-slow', '1x1', ['C-slow']), ('C-shutdown', '1x1', ['C-shutdown']), ('C-asbuilt', '1x1', ['C-asbuilt'])):
    spec = json.loads((Path(sys.argv[3]) / label / 'build.json').read_text())
    groups = scenario.all_groups(scenario.point(point, spec), spec) + scenario.boot_fault_groups()
    for g in groups:
        recorded = [runs / d / f'{g.name}.txt' for d in dirs if (runs / d / f'{g.name}.txt').exists()]
        if not recorded:
            print(f'{label} {g.name}: not recorded in round 2')
            continue
        same = recorded[0].read_text() == g.script()
        print(f'{label} {g.name}: {"identical" if same else "CHANGED"} ({recorded[0].parent.name})')
