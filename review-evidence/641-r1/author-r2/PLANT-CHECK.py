"""Check patch applicability and the receive-filter mutation anchors."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path.cwd()
base = '759d1d248fad095ab07bfcc480a0828117501f39'
source = 'hdl/ieee8021q/filtering/rx_mac_filter.sv'
before = subprocess.check_output(['git', 'show', base + ':' + source], text=True)
after = (root / source).read_text()
pattern = re.compile(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/', re.S)
def code(text):
    return pattern.sub(lambda m: m[0] if m[0].startswith('"') else '', text)
assert code(before) == code(after), 'functional RTL changed'
spec = importlib.util.spec_from_file_location('binding', root / 'tb/verilator/rx_filter/binding_mutant.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
rows = []
for name, path, old, new, marker in module.ARMS:
    text = path.read_text()
    assert text.count(old) == 1, name
    assert text.replace(old, new, 1) != text, name
    rows.append(dict(name=name, source=str(path.resolve().relative_to(root)), occurrences=1))
patches = sorted((root / 'tb').rglob('*.patch'))
for path in patches:
    subprocess.run(['git', 'apply', '--check', str(path)], check=True)
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
print(json.dumps(dict(head=head, functional_rtl_unchanged=True, patches_checked=len(patches), anchors=rows), indent=2))
