"""Grade illegal/legal synthesis-example receipts from both converters."""
import json
import os
from pathlib import Path

work = Path(os.environ['WORK'])
rows = []
for version, marker in [('sv2v12', 'rx_mac_filter: TDATA_WIDTH='), ('sv2v13', '$error')]:
    results = json.loads((work / 'docs-example' / version / 'results.json').read_text())
    assert len(results) == 2
    illegal, legal = results
    assert illegal['point'] == 'rx-tdata-52'
    assert illegal['rc'] != 0 and marker in illegal['first_error'], illegal
    assert legal['point'] == 'rx-tdata-52-legal64' and legal['rc'] == 0, legal
    rows.extend(results)
print(json.dumps(rows, indent=2))
