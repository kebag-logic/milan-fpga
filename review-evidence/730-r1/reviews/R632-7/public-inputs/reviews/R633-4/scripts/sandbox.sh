#!/usr/bin/env python3
"""Run each unchanged mutation driver's candidate in a disposable namespace.

No network, host credentials, Docker socket or privileged operation is exposed.
Keep per-mutant raw output without altering exit status.
"""
import os
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent.parent
tree = Path(sys.argv[1]).resolve()
mode = 'selftest' if '--selftest' in sys.argv else 'probe'
ident = tree.name
assert ident[0] in 'KQ' and ident[1:].isdigit(), ident
temporary = packet / 'scratch' / 'tmp' / ident
temporary.mkdir(parents=True, exist_ok=True)
command = [
    'bwrap', '--unshare-all', '--die-with-parent', '--new-session',
    '--ro-bind', '/usr', '/usr', '--symlink', 'usr/bin', '/bin',
    '--symlink', 'usr/sbin', '/sbin', '--symlink', 'usr/lib', '/lib',
    '--symlink', 'usr/lib64', '/lib64',
    '--ro-bind', '/etc/ld.so.cache', '/etc/ld.so.cache',
    '--ro-bind', '/etc/passwd', '/etc/passwd',
    '--ro-bind', '/etc/group', '/etc/group',
    '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/run', '--tmpfs', '/home',
    '--bind', str(tree), str(tree),
    '--ro-bind', str(packet / 'scripts'), str(packet / 'scripts'),
    '--bind', str(temporary), '/tmp', '--chdir', str(tree),
    '--clearenv', '--setenv', 'PATH', '/usr/bin:/bin',
    '--setenv', 'HOME', '/tmp/home', '--setenv', 'TMPDIR', '/tmp',
    '--setenv', 'LANG', 'C.UTF-8', '--setenv', 'PYTHONDONTWRITEBYTECODE', '1',
    *sys.argv[2:],
]
result = subprocess.run(command, capture_output=True)
out = packet / 'receipts' / 'mutant-logs'
out.mkdir(exist_ok=True)
(out / f'{ident}-{mode}.stdout').write_bytes(result.stdout)
(out / f'{ident}-{mode}.stderr').write_bytes(result.stderr)
(out / f'{ident}-{mode}.rc').write_text(f'{result.returncode}\n')
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
