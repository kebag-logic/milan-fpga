import concurrent.futures
import json
from pathlib import Path
import urllib.request

PACKET = Path(__file__).resolve().parent
PREFIX = 'review-evidence/737-image-r1/'
REV = 'dedfaa3fce9db0b1e7ac2b10ec970f5158fff756'
if not (PACKET / 'scratch/evidence-tree.json').exists():
    (PACKET / 'scratch').mkdir(exist_ok=True)
    with urllib.request.urlopen(f'https://api.github.com/repos/kebag-logic/milan-fpga/git/trees/{REV}?recursive=1', timeout=90) as response:
        (PACKET / 'scratch/evidence-tree.json').write_bytes(response.read())
TREE = json.loads((PACKET / 'scratch/evidence-tree.json').read_text())['tree']
selected = [x['path'] for x in TREE if x['type'] == 'blob' and (
    x['path'] == PREFIX + 'MANIFEST.json' or
    x['path'].startswith(PREFIX + 'author-r8/round8-') and
    not any(s in x['path'] for s in ('collector', 'builder.py', 'rules.py')))]

def fetch(path):
    out = PACKET / 'evidence' / path.removeprefix(PREFIX)
    out.parent.mkdir(parents=True, exist_ok=True)
    url = f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{REV}/{path}'
    with urllib.request.urlopen(url, timeout=90) as response:
        out.write_bytes(response.read())
    return path

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, selected))
print(f'Downloaded {len(results)} public evidence files at {REV}')
