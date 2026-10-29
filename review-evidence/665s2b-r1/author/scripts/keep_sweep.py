#!/usr/bin/env python3
"""Scratch: copy the four-shard sweep's receipts, scrubbing host paths. A file over 200 KB is not copied; its
sha256 and size go to large-files.txt. Writes tally.md: each shard's suites, checks and failures from its summary.

usage: keep_sweep.py SWEEP_DIR OUT_DIR"""
import hashlib
import json
import re
import sys
from pathlib import Path

LIMIT = 200 * 1024
SCRUB = ((re.compile(r'$VALIDATION_STORAGE/665s2b-a683l'), '<scratch>'), (re.compile(r'$LANES/'), '<lanes>/'),
         (re.compile(r'$VALIDATION_TOOLS'), '<tools>'), (re.compile(r'$WORKSPACE_HOME'), '<home>'))


def scrub(text: str) -> str:
    for pattern, repl in SCRUB:
        text = pattern.sub(repl, text)
    return text


def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    large, rows = [], ['| Shard | Suites | Passed | Failed | Timed out | Checks | In-suite failures | Seconds | rc |',
                       '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for f in sorted(p for p in src.rglob('*') if p.is_file()):
        rel = f.relative_to(src)
        data = f.read_bytes()
        if len(data) > LIMIT:
            large.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}')
            continue
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            dest.write_text(scrub(data.decode()))
        except UnicodeDecodeError:
            dest.write_bytes(data)
    for k in range(4):
        shard = src / f'shard-{k}'
        log = (shard / 'spec/01.log').read_text()
        s = re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)', log)
        c = re.search(r'checks: (\d+)\s+in-suite failures: (\d+)', log)
        res = json.loads((shard / 'spec/results.json').read_text())['results'][0]
        rows.append(f"| {k}/4 | {s[1]} | {s[2]} | {s[3]} | {s[4]} | {int(c[1]):,} | {c[2]} | {res['seconds']:.0f} | "
                    f"{res['exit_code']} |")
    (out / 'large-files.txt').write_text('\n'.join(large) + '\n')
    (out / 'tally.md').write_text('\n'.join(rows) + '\n')
    print('\n'.join(rows))
    print(f'{len(large)} file(s) over 200 KB recorded by sha256 and size')
    return 0


if __name__ == '__main__':
    sys.exit(main())
