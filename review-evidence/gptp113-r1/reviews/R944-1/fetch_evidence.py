#!/usr/bin/env python3
"""Issue #113: reconstruct only the frozen public evidence packet."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

PIN = 'dcfe275da410b7caf1f914697cd2dc68fbd5349f'
ROOT = f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{PIN}/review-evidence/gptp113-r1/'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('packet', type=Path)
    parser.add_argument('--jobs', type=int, default=4, choices=range(1, 17))
    args = parser.parse_args()
    scratch = args.packet.resolve() / 'scratch'
    scratch.mkdir(exist_ok=True)
    with urlopen(ROOT + 'MANIFEST.json', timeout=60) as response:
        manifest = response.read()
    (scratch / 'consumer-manifest.json').write_bytes(manifest)
    def one(entry):
        rel = Path(entry['file'])
        assert rel.parts[0] == 'author' and '..' not in rel.parts
        with urlopen(ROOT + rel.as_posix(), timeout=60) as response:
            data = response.read()
        assert hashlib.sha256(data).hexdigest() == entry['published_sha256']
        dest = scratch / 'public-author' / Path(*rel.parts[1:])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return rel.as_posix()
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        paths = list(pool.map(one, json.loads(manifest)))
    print('Verified public files:', len(paths), 'at', PIN)


if __name__ == '__main__':
    main()
