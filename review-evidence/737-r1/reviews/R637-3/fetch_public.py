#!/usr/bin/env python3
"""Fetch only the public author receipts used by the source audit."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

REV = '8fc0bb247606c9eb1eeeebc57e26a4df1f549790'
BASE = 'review-evidence/737-r1/author-r3/'
NAMES = ('round3-source-sizing.json', 'round3-committed-gates.json',
         'round3-worker-projections.json', 'round3-fresh-collector.json',
         'round3-contract-timing.json', 'round3-runner-timing.json',
         'round3-dispatcher-build.json', 'round3-committed-gates-resources.json',
         'round2-case-evidence/comparison-summary.json')

def main():
    packet = Path(__file__).resolve().parent
    target = packet / 'scratch/public-evidence'
    target.mkdir(parents=True, exist_ok=True)
    def fetch(name):
        path = BASE + name
        data = subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/contents/' + path +
                                        '?ref=' + REV, '-H', 'Accept: application/vnd.github.raw+json'])
        (target / name).parent.mkdir(parents=True, exist_ok=True)
        (target / name).write_bytes(data)
        return {'path': path, 'url': 'https://github.com/kebag-logic/milan-fpga/blob/' + REV + '/' + path,
                'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch, NAMES))
    (packet / 'public-receipt-index.json').write_text(json.dumps(rows, indent=2) + '\n')
    print('Fetched and hashed', len(rows), 'public receipts at', REV)

if __name__ == '__main__':
    main()
