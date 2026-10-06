import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

work = Path(__file__).parent
repo = Path(os.environ['REPO'])
gate = work / 'route/ax7101/gateware'
source = (gate / 'alinx_ax7101.tcl').read_text()
paths = {Path(p) for p in re.findall(r'^read_verilog (?:-v )?\{([^}]+)\}', source, re.M)}
assert paths
for value in re.findall(r'-include_dirs \{([^}]+)\}', source):
    for directory in value.split():
        paths.update(Path(directory).glob('*.svh'))
        paths.update(Path(directory).glob('*.vh'))
paths.update(Path(row['path']) for row in json.loads((gate / 'baseline_images.json').read_text()))
paths.update([gate / 'alinx_ax7101.tcl', gate / 'alinx_ax7101.xdc', gate / 'baseline_integrated.tcl'])
records = []
for path in sorted(paths):
    data = path.read_bytes()
    name = str(path).replace(str(repo), '$REPO').replace(str(work), '$WORK')
    name = name.replace(str(Path.home()), '$HOME')
    records.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
result = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip(),
          'inventory': 'Every read_verilog source, all headers in declared include directories, '
                       'all inventoried memory images, export/prepared Tcl and XDC', 'files': records}
destination = work / ('source-inputs-after.json' if '--verify' in sys.argv else 'source-inputs-before.json')
if '--verify' in sys.argv:
    assert result == json.loads((work / 'source-inputs-before.json').read_text())
destination.write_text(json.dumps(result, indent=2) + '\n')
print('Verified' if '--verify' in sys.argv else 'Recorded', len(records), 'implementation inputs')
