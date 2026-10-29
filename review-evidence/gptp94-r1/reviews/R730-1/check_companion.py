#!/usr/bin/env python3
"""Check the public companion against its public base, without a parent build."""
import hashlib
from pathlib import Path
import re
import subprocess

packet = Path(__file__).resolve().parent
patch = packet / 'public/author/milan-fpga-companion.patch'
work = packet / 'scratch' / 'parent-patch'
work.mkdir(parents=True, exist_ok=True)

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

with (packet / 'companion-check.log').open('w') as log:
    count = 0
    for section in patch.read_text().split('diff --git ')[1:]:
        name = section.splitlines()[0].split(' b/')[1]
        old, new, mode = re.search(r'^index ([0-9a-f]+)\.\.([0-9a-f]+) (\d+)$', section, re.M).groups()
        if mode == '160000':
            assert name == 'gptp-processor'
            assert '-Subproject commit f97c18035be6ef5345e5af27db2124c5697c1b40' in section
            assert '+Subproject commit 9d509029de967c50de7527edf2b8869aa9db9074' in section
            print('PASS exact old/new gptp-processor gitlinks', file=log)
            continue
        data = (packet / 'public/parent' / name).read_bytes()
        if not blob(data).startswith(old) and blob(data[:-1]).startswith(old):
            data = data[:-1]
        assert blob(data).startswith(old), name
        dest = work / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print('PASS preimage', name, blob(data), file=log)
        count += 1
    for option in ['--check', '--apply']:
        r = subprocess.run(['git', 'apply', option, '--exclude=gptp-processor', str(patch)], cwd=work, stdout=log, stderr=subprocess.STDOUT)
        assert r.returncode == 0
    for section in patch.read_text().split('diff --git ')[1:]:
        name = section.splitlines()[0].split(' b/')[1]
        old, new, mode = re.search(r'^index ([0-9a-f]+)\.\.([0-9a-f]+) (\d+)$', section, re.M).groups()
        if mode != '160000':
            assert blob((work / name).read_bytes()).startswith(new), name
            print('PASS patched blob', name, file=log)
    print('PASS companion applied; verified files:', count, file=log)
print('Parent companion patch: PASS')
