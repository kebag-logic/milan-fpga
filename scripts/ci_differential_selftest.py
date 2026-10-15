#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Hold the census gate: only shapes proven by a differential fixture are accepted.

The committed receipt is checked against the fixtures, then planted trees show the
gate refusing by name: a shape outside the census, a receipt measured at another
walker, and a census shape whose focus fixture did not meet its expectation.
"""

import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile

import yaml

import ci_command_table
import ci_differential
import ci_tool_inventory as inventory


def derive(root: Path, step: str) -> str:
    """Run --write with the gate on; return the output."""
    (root / '.github/workflows/fixture.yml').write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [{'run': step}]}}}))
    saved = sys.argv
    output = io.StringIO()
    try:
        sys.argv = ['ci_tool_inventory.py', '--root', str(root), '--write']
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            rc = inventory.main()
    finally:
        sys.argv = saved
    return f'{rc}: {output.getvalue()}'


def main() -> int:
    """The receipt meets every expectation; the gate refuses what it does not prove."""
    assert ci_differential.check() == 0
    assert ci_command_table.GATE
    census = json.loads(ci_differential.CENSUS.read_text())['shapes']
    used = ci_differential.tree_shapes()
    assert set(census) == set(used), (sorted(set(census) - set(used)), sorted(set(used) - set(census)))
    print(f'PASS: the census is exactly the {len(used)} shapes the tree applies')
    with tempfile.TemporaryDirectory(prefix='ci-gate-') as directory:
        root = Path(directory)
        (root / 'ci/image').mkdir(parents=True)
        (root / '.github/workflows').mkdir(parents=True)
        for name in ('command-table.json', 'sources.lock.json', 'syntax-census.json', 'make-builtins.json',
                     'differential-receipt.json'):
            shutil.copyfile(inventory.ROOT / 'ci/image' / name, root / 'ci/image' / name)
        result = derive(root, 'zz_probe() { :; }\nzz_probe\n')
        assert result.startswith('0:'), result
        print('PASS: census shapes proven by the receipt are accepted')
        result = derive(root, 'X="a b"\necho $X\n')
        assert result.startswith('2:') and "uncensused construct shape 'bash:word.split'" in result, result
        print('PASS: a shape the tree does not use refuses by name')
        receipt_path = root / 'ci/image/differential-receipt.json'
        receipt = json.loads(receipt_path.read_text())
        stale = dict(receipt, binding='0' * 64)
        receipt_path.write_text(json.dumps(stale))
        result = derive(root, 'echo okay\n')
        assert result.startswith('2:') and 'differential receipt does not match' in result, result
        print('PASS: a receipt measured at another walker refuses')
        unmet = json.loads(json.dumps(receipt))
        unmet['fixtures']['bash-pipe']['outcome'] = 'mismatch'
        receipt_path.write_text(json.dumps(unmet))
        result = derive(root, 'echo a | cat\n')
        assert result.startswith('2:') and "uncensused construct shape 'bash:pipe'" in result, result
        print('PASS: a shape whose focus fixture did not meet its expectation refuses')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
