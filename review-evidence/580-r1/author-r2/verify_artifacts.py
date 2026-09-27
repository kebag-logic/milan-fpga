"""Rebuild all shipping artifacts against the public round-1 hash table."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
BUILD = Path('/tmp/580-a368/artifact-check')
body = subprocess.check_output(['rtk', 'proxy', 'gh', 'api',
    'repos/kebag-logic/milan-fpga/issues/comments/5856703787', '--jq', '.body'], text=True)
expected = {}
for name, table in re.findall(r'### (endstation_\w+)\n(.*?)(?=\n### |\n</details>)', body, re.S):
    for leaf, size, sha in re.findall(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|', table):
        expected[name + '/' + leaf] = dict(bytes=int(size), sha256=sha)
assert len(expected) == 65, len(expected)
results = {}
commands = []
for cfg in sorted((ROOT/'configs').glob('endstation_*.yaml')):
    name = cfg.stem
    dest = BUILD/name
    commands.extend([
        [sys.executable, 'sw/builder/endstation_builder.py', str(cfg.relative_to(ROOT)), '-o', str(dest/'builder')],
        [sys.executable, 'avdecc/gen_aemi_image.py', '--overlay', str(dest/'builder'/name/'aem_overlay.json'),
         '--line-bytes', '576', '-o', str(dest/'aem.bin'), '-m', str(dest/'aem.map'), '--json', str(dest/'aem.json')]])
    for command in commands[-2:]:
        subprocess.run(['rtk', 'proxy', *command], check=True, timeout=600)
    files = {p.name: p for p in dest.glob('aem.*')}
    files.update({'builder/'+p.name: p for p in (dest/'builder'/name).iterdir() if p.is_file()})
    for leaf, path in files.items():
        data = path.read_bytes()
        results[name+'/'+leaf] = dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
assert results == expected, {k: (expected.get(k), results.get(k)) for k in expected.keys() | results.keys() if expected.get(k) != results.get(k)}
receipt = dict(reference='https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5856703787',
               commands=commands, files=results, result='All 65 files match the public old-pin/new-pin equality table')
(OUT/'current-artifacts.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(receipt['result'])
