"""Compare retained delayed controls with the read-only reviewer plants."""
from pathlib import Path
import hashlib
import json
import runpy

ROOT = Path('$LANES/602-phc-step-mr')
OUT = Path(__file__).resolve().parent
review = runpy.run_path('$REVIEWS/602-r366-2-packet/probes.py')
current = runpy.run_path(str(ROOT / 'tb/verilator/milan_dp/gmstep_mutants.py'))
source = (ROOT / 'hdl/milan/milan_datapath.sv').read_text()
rows = []
for delay, name in ((16, 'O4_adjtime_delay16'), (256, 'O5_adjtime_delay256')):
    leg, edits = review['PROBES'][name]
    expected = source
    for anchor, replacement in edits:
        assert expected.count(anchor) == 1
        expected = expected.replace(anchor, replacement)
    control_name = f'PHC adjtime becomes an mr cause {delay} cycles later'
    control, = [c for c in current['CONTROLS'] if c.name == control_name]
    assert source.count(control.anchor) == 1
    actual = source.replace(control.anchor, control.replacement)
    assert actual == expected and control.leg == leg == 'option-off'
    rows.append({'reviewer_probe': name, 'control': control_name,
                 'bytes': len(actual.encode()),
                 'sha256': hashlib.sha256(actual.encode()).hexdigest(),
                 'byte_identical_planted_source': True})
(OUT / 'probe-equivalence-result.json').write_text(json.dumps(rows, indent=2) + '\n')
print('PASS: both delayed controls produce byte-identical reviewer plants.')
