#!/usr/bin/env python3
"""Usage: python3 probe-delta.py SOURCE PACKET. All mutations stay in scratch."""
import os
from pathlib import Path
import subprocess
import sys

source, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
root = scratch / 'probe-source'
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
head = '0ea635ea22eeb6d97335c4e814eede1ac0d67ebc'
subprocess.run(['git', 'clone', '--quiet', '--shared', '--no-hardlinks', str(source), str(root)], check=True)
subprocess.run(['git', 'checkout', '--quiet', '--detach', head], cwd=root, check=True)

def run(name, command, want, tokens=()):
    p = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (packet / (name + '.log')).write_text(p.stdout)
    (packet / (name + '.rc')).write_text(str(p.returncode) + '\n')
    assert p.returncode == want, (name, p.returncode, p.stdout)
    assert all(t in p.stdout for t in tokens), (name, tokens, p.stdout)
    print(name, 'rc', p.returncode, 'expected', want, flush=True)

gate = ['make', '-j16', 'inventory']
run('inventory-clean', gate, 0, ('25 cases, OK', '63 Markdown files, OK'))
cases = [
    ('fake-op', 'hdl/aecp/ucpu_pkg.sv', '  } ucpu_op_e;', "    , OP_REVIEW_FAKE = 5'd30\n  } ucpu_op_e;", None),
    ('drop-target-row', 'docs/architecture/09_verification.md', None, None, ('table lacks `inventory`',)),
    ('drop-check-prerequisite', 'Makefile', 'figures inventory stale\n', 'figures stale\n', ('table names `inventory`, which `check` does not run',)),
    ('old-uisa', 'docs/architecture/06_aecp_engine.md', None, None, ('says 29 operations', 'table lacks SHIFT_R')),
]
for name, path, old, new, tokens in cases:
    file = root / path
    original = file.read_bytes()
    body = original.decode()
    try:
        if name == 'fake-op':
            # Keep valid SV syntax and the defining file's normal member form.
            body = body.replace("OP_SHIFT_R    = 5'd29   //", "OP_SHIFT_R    = 5'd29,  //")
            body = body.replace('  } ucpu_op_e;', "    OP_REVIEW_FAKE = 5'd30\n  } ucpu_op_e;")
            tokens = ('says 30 operations, the enum declares 31', 'table lacks REVIEW_FAKE')
        elif name == 'drop-target-row':
            body = ''.join(line for line in body.splitlines(keepends=True) if not line.startswith('| `inventory` |'))
        elif name == 'old-uisa':
            body = body.replace('**µISA (30 operations)**', '**µISA (29 operations)**').replace(', `SHIFT_R` |', ' |')
        else:
            assert old in body
            body = body.replace(old, new)
        assert body.encode() != original
        file.write_text(body)
        run(name, gate, 2, tokens)
    finally:
        file.write_bytes(original)
run('inventory-restored', gate, 0, ('63 Markdown files, OK',))
run('links', ['make', '-j16', 'links'], 0)
run('probe-restored-diff', ['git', 'diff', '--exit-code', head], 0)
print('All mutations rejected; tracked bytes restored.', flush=True)
