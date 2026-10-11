#!/usr/bin/env python3
"""List the explicit publishable packet; scratch and other reviewers' reports stay out."""
import hashlib
from pathlib import Path
import sys


def main():
    packet = Path(sys.argv[1]).resolve()
    excluded = {'issue-151.json', 'issue-151-comments.json', 'pr-175-comments.json',
                'pr-175-comments-final.json', 'pr-175-metadata.json'}
    files = []
    for base in ('scripts', 'receipts'):
        for path in sorted((packet / base).rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            if path.name in excluded or path.name.startswith('prior-public-'):
                continue
            # Only the public identity excerpt of the long author handoff is republished.
            if path.name == 'HANDOFF.md':
                continue
            files.append(path)
    files.append(packet / 'REPORT.md')
    lines = [f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(packet).as_posix()}'
             for path in sorted(files)]
    (packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
    assert not any('scratch/' in line for line in lines)
    print(f'{len(lines)} publishable files listed; no scratch tree or other reviewer report listed')


if __name__ == '__main__':
    main()
