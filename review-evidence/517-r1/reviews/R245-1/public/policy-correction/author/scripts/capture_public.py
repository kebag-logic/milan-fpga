#!/usr/bin/env python3
"""Archive only public issue records and immutable linked original evidence."""
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parents[1] / 'public'
API = 'repos/kebag-logic/milan-fpga/'
AUTHOR = '30fc230e8df8ca32499c6e1bd294bfe0cdb38983'
FAILURE = '6d68faf6720e2af0cb96ab64984e7bcf77a3e758'
ITEMS = (
    ('issue517.json', ['issues/517']),
    ('issue517-comments.json', ['issues/517/comments?per_page=100']),
    ('issue259.json', ['issues/259']),
    ('decision.json', ['issues/comments/5781783857']),
    ('original-HANDOFF.md', ['contents/review-evidence/517-r1/author/HANDOFF.md?ref=' + AUTHOR]),
    ('original-failure-29.log', ['contents/review-evidence/517-r1/source-first-failure/29.log?ref=' + FAILURE]),
    ('original-partial-results.json', ['contents/review-evidence/517-r1/source-first-failure/partial-results.json?ref=' + FAILURE]),
)


def main():
    receipts = []
    for name, endpoints in ITEMS:
        argv = ['rtk', 'proxy', 'gh', 'api']
        if endpoints[0].startswith('contents/'):
            argv += ['-H', 'Accept: application/vnd.github.raw+json']
        argv.append(API + endpoints[0])
        result = subprocess.run(argv, capture_output=True, check=False)
        (OUT / name).write_bytes(result.stdout)
        assert result.returncode == 0, (argv, result.stderr)
        receipts.append(dict(file=name, argv=argv, exit=result.returncode,
                             sha256=hashlib.sha256(result.stdout).hexdigest()))
    (OUT / 'receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps(receipts, indent=2))


if __name__ == '__main__':
    main()
