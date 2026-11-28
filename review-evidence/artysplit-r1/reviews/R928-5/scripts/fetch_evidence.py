#!/usr/bin/env python3
"""Materialize only the pinned public author evidence (rounds 10 and 11 and the outer manifest); never reviewer reports.

usage: python3 -I fetch_evidence.py REPO OUT
"""
import subprocess
import sys
import tarfile
from pathlib import Path

REF = '3e8f3014f28d13bd008b06ec43f919d282d681ee'
BASE = 'review-evidence/artysplit-r1'
PATHS = [f'{BASE}/MANIFEST.json', f'{BASE}/author-r10', f'{BASE}/author-r11']


def main(repo: Path, out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(['git', '-C', str(repo), 'archive', REF, *PATHS], stdout=subprocess.PIPE)
    count = size = 0
    with tarfile.open(fileobj=proc.stdout, mode='r|') as archive:
        for member in archive:
            if not member.isfile():
                continue
            relative = Path(member.name).relative_to(BASE)
            assert '..' not in relative.parts and not relative.is_absolute()
            target = out / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as src, target.open('wb') as dst:
                while chunk := src.read(1 << 20):
                    dst.write(chunk)
            count += 1
            size += member.size
    assert proc.wait() == 0
    print(f'PASS extracted {count} files, {size} bytes from {REF}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
