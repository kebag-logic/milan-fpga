#!/usr/bin/env python3
"""A copy of a compact census extract (hard links) whose census.json omits one case; every other byte unchanged.

usage: python3 -I prepare_control.py EXTRACT OUT CASE
"""
import json
import os
import sys
from pathlib import Path


def main(src: Path, out: Path, case: str) -> int:
    count = 0
    for path in src.rglob('*'):
        if path.is_file() and path.name != 'census.json':
            target = out / path.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(path, target)
            count += 1
    census = json.loads((src / 'census.json').read_text())
    kept = [r for r in census['cases'] if r['case'] != case]
    assert len(kept) == len(census['cases']) - 1, case
    census['cases'] = kept
    (out / 'census.json').write_text(json.dumps(census, indent=1) + '\n')
    print(f'PASS control: {count} files hard-linked unchanged; census.json lists {len(kept)} cases without {case}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]))
