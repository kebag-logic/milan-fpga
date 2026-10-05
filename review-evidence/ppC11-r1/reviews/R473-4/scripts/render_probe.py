#!/usr/bin/env python3
"""Check margin geometry, rejected margins and stale-export detection."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import wavedrom

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
a = p.parse_args()
spec = importlib.util.spec_from_file_location('renderer', a.source / 'scripts/render-wavedrom.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
failures = 0
for path, anchor, src in m.collect_blocks():
    if anchor not in ['fig-02-txwave', 'fig-02-memwave']:
        continue
    data = json.loads(src)
    raw = ET.fromstring(wavedrom.render(src).tostring())
    base = list(map(float, raw.attrib['viewBox'].replace(',', ' ').split()))
    children = [ET.tostring(c) for c in raw]
    for margin in [0, 1, 40, 80]:
        data['config']['svg_margin'] = margin
        rendered = ET.fromstring(m.render_svg(json.dumps(data)))
        box = list(map(float, rendered.attrib['viewBox'].replace(',', ' ').split()))
        expected = [base[0] - margin, base[1], base[2] + 2 * margin, base[3]]
        good = box == expected and [ET.tostring(c) for c in rendered] == children
        print(json.dumps({'anchor': anchor, 'margin': margin, 'box': box, 'unchanged_children': good}))
        failures += not good
    for margin in [-1, 0.5, '40', True, None]:
        data['config']['svg_margin'] = margin
        try:
            m.render_svg(json.dumps(data))
            good = False
        except ValueError as exc:
            good = 'config.svg_margin must be a non-negative integer' in str(exc)
        print(json.dumps({'anchor': anchor, 'invalid_margin': margin, 'rejected': good}))
        failures += not good
    data['config'].pop('svg_margin')
    good = m.render_svg(json.dumps(data)) == wavedrom.render(json.dumps(data)).tostring()
    print(json.dumps({'anchor': anchor, 'default_render_identical': good}))
    failures += not good
# Execute the freshness gate after removing source margins in the disposable clone.
path = a.source / 'docs/architecture/02_interfaces.md'
original = path.read_bytes()
try:
    text = original.decode().replace(' "config": {"svg_margin": 40},\n', '')
    assert text != original.decode()
    path.write_text(text)
    r = subprocess.run([sys.executable, str(a.source / 'scripts/render-wavedrom.py'), '--check'],
                       text=True, capture_output=True)
    good = r.returncode == 1 and 'fig-02-txwave' in r.stdout and 'fig-02-memwave' in r.stdout
    print(json.dumps({'mutation': 'remove-source-margins', 'rc': r.returncode, 'killed': good, 'stdout': r.stdout}))
    failures += not good
finally:
    path.write_bytes(original)
print(f'Margin probe failures: {failures}')
raise SystemExit(bool(failures))
