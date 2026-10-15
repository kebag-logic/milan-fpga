#!/usr/bin/env python3
"""Write a minimal, valid pure-Python wheel (no build backend needed) for an offline install control."""
import base64, hashlib, sys, zipfile
out = sys.argv[1]
files = {'zz_probe_pkg/__init__.py': b'VALUE = 1\n',
         'zz_probe_pkg-0.1.dist-info/METADATA': b'Metadata-Version: 2.1\nName: zz-probe-pkg\nVersion: 0.1\n',
         'zz_probe_pkg-0.1.dist-info/WHEEL': b'Wheel-Version: 1.0\nGenerator: reviewer\nRoot-Is-Purelib: true\nTag: py3-none-any\n'}
record = ''.join(f"{n},sha256={base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b'=').decode()},{len(b)}\n" for n, b in files.items())
record += 'zz_probe_pkg-0.1.dist-info/RECORD,,\n'
with zipfile.ZipFile(out, 'w') as z:
    for n, b in files.items():
        z.writestr(n, b)
    z.writestr('zz_probe_pkg-0.1.dist-info/RECORD', record)
