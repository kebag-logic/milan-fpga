"""Build compact control and gate tables from final candidate receipts."""
from pathlib import Path
import json
import re
import shlex

OUT = Path(__file__).resolve().parent
HEAD = '471892a9bcc2d26fdcfc19db01949ecea83c5e0f'
ROOT = '$LANES/602-phc-step-mr'

def record(name):
    data = json.loads((OUT/(name+'.json')).read_text())
    assert data['head'] == HEAD and data['rc'] == 0, name
    return data

text = Path(record('gmstep-mutants')['log']).read_text()
rows = re.findall(r'\[PASS\] control caught: (.*?) - breaks "(.*?)"\n    it broke (\d+) check\(s\): (.*)', text)
assert len(rows) == 18, len(rows)
controls = ['| Control | Required failure | Observed failures |', '|---|---|---|']
for name, required, count, observed in rows:
    controls.append(f'| {name} | {required} | {count}: {observed} |')
(OUT/'controls-table.md').write_text('\n'.join(controls)+'\n')
names = ['rtl-lint', 'ci-scope', 'baremetal-check', 'baremetal-selftest', 'docs',
         'doc-style', 'doc-style-selftest', 'em-dash', 'doc-paths', 'toc', 'toc-selftest',
         'gptp-docs', 'feature-status', 'solution-docs', 'submodule-docs', 'module-matrix',
         'diagram-pngs', 'archive', 'source-lists', 'sv-idiom', 'cpp-idiom', 'py-idiom',
         'hygiene', 'test-evidence', 'diff-check', 'milan-dp', 'tkdiag', 'gmstep-mutants',
         'builder-rv32', 'builder-absent', 'ooc-after', 'artifact-identity',
         'stale-doc-rescan', 'candidate-audit']
gates = ['| Gate / receipt | Command | Timeout (s) | Elapsed (s) | rc |', '|---|---|---:|---:|---:|']
for name in names:
    data = record(name)
    command = shlex.join(data['command']).replace(ROOT, '$ROOT').replace(str(OUT), '$PACKET')
    gates.append(f"| `{name}.json` | `{command}` | {data['timeout']} | {data['seconds']} | {data['rc']} |")
(OUT/'gates-table.md').write_text('\n'.join(gates)+'\n')
print(f'{len(rows)} control rows; {len(names)} successful final-head gate rows.')
