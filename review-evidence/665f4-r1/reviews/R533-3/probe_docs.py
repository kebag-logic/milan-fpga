#!/usr/bin/env python3
"""Drop the new dependency from each documentation boundary in disposable data."""
import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
a=p.parse_args(); root=a.repo.resolve(); packet=a.packet.resolve()
sys.path.insert(0,str(root/'scripts'))
import check_submodule_docs as gate
paths=gate.configured_paths(); pins=gate.gitlink_pins(paths)
rows=gate.parse_rows((root/'docs/reference/SUBMODULES.md').read_text())
assert not gate.validate_rows(rows,pins)
assert not gate.validate_drawio(paths)
missing=gate.validate_rows([r for r in rows if r.path!='third_party/lwSRP'],pins)
assert 'missing paths: third_party/lwSRP' in missing
diagram=ET.parse(root/'docs/diagrams/submodule_boundaries.drawio')
for parent in diagram.iter():
    for child in list(parent):
        if child.get('id')=='sub-third_party-lwSRP' or child.get('source')=='sub-third_party-lwSRP':
            parent.remove(child)
out=packet/'scratch/docs-missing-lwsrp.drawio'; diagram.write(out)
node=gate.validate_drawio(paths,out)
assert 'third_party/lwSRP: Draw.io node is missing or mislabeled' in node
assert 'Draw.io edges do not cover every submodule exactly once' in node
result={'baseline':'PASS','missing_inventory':'KILLED','inventory_diagnostics':missing,
        'missing_diagram_node_and_edge':'KILLED','diagram_diagnostics':node}
(packet/'docs-plants.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
