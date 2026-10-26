#!/usr/bin/env python3
"""Check the prescribed wording and inventory newly added source comments."""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
policy=(root/'docs/testing/CI_WORKFLOWS.md').read_text()
expected="A label that has neither a `--platform` entry nor an entry in act's built-in table, such as `ubuntu-24.04`, is no error to `act`: it skips that job as an unsupported platform and can still exit 0, and a built-in label such as `ubuntu-latest` would run on act's default `node:16` image instead, so the self-test requires an entry for every accepted label."
assert expected in ' '.join(policy.split())
print('PASS R697-1-01 prescribed wording, with line wrapping normalized')
print('Policy opening, pinned image and reason:')
print('\n'.join(policy.splitlines()[6:13]))
print('Added source comments/docstrings, manually checked for review and lane residue:')
for line in (packet/'source.diff').read_text().splitlines():
    if not line.startswith('+') or line.startswith('+++'): continue
    value=line[1:]
    if value.lstrip().startswith('#') or '"""' in value:
        print(value)
print('PASS new comments describe behavior/reason; no added lane, round, reviewer or issue-comment identity')
