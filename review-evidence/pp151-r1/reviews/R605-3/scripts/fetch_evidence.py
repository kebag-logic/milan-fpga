#!/usr/bin/env python3
"""Read only public author receipts at the published evidence commit."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys

COMMIT = '14f8fe421ca8699bcba10968c8e6a8abd09b343b'
PREFIX = 'review-evidence/pp151-r1/author-r2/'


def main():
    packet = Path(sys.argv[1]).resolve()
    tree = json.loads((packet / 'receipts/public-evidence-tree.json').read_text())
    selected = []
    for item in tree:
        if item['type'] != 'blob' or not item['path'].startswith(PREFIX):
            continue
        rel = item['path'][len(PREFIX):]
        keep = rel == 'parent-guard-evidence.patch'
        keep |= rel.startswith('evidence/round2/') and rel.count('/') <= 3
        keep |= rel.startswith(('evidence/bench/', 'evidence/netlists/', 'evidence/scripts/'))
        keep |= rel.startswith('evidence/campaigns/compare/')
        keep |= rel.startswith('evidence/records/') and not rel.endswith('.env')
        if keep:
            selected.append(item)
    def get(item):
        rel = item['path'][len(PREFIX):]
        target = packet / 'receipts/public-author' / rel
        if not target.exists():
            result = subprocess.run(['gh', 'api', 'repos/kebag-logic/milan-fpga/git/blobs/' + item['sha']],
                                    capture_output=True, check=True, text=True)
            data = base64.b64decode(json.loads(result.stdout)['content'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        data = target.read_bytes()
        sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert sha == item['sha'], rel
        return {'path': str(target.relative_to(packet)), 'git_blob': sha,
                'sha256': hashlib.sha256(data).hexdigest(),
                'url': f'https://github.com/kebag-logic/milan-fpga/blob/{COMMIT}/{item["path"]}'}
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(get, selected))
    (packet / 'receipts/public-author-fetch.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} public author files downloaded; every git blob verified')


if __name__ == '__main__':
    main()
