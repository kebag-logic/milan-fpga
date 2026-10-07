#!/usr/bin/env python3
"""Build the unit dependency in PACKET/scratch; no shared installation."""
from pathlib import Path
import hashlib
import io
import json
import subprocess
import sys
import tarfile
p=Path(sys.argv[1]).resolve()
s=p/'scratch/unit-dependency'
b=p/'scratch/unit-dependency-build'
s.mkdir(parents=True,exist_ok=True)
if not (s/'CMakeLists.txt').exists():
    archive=subprocess.check_output(['rtk','proxy','gh','api','repos/cgreen-devs/cgreen/tarball/1.7.0'])
    assert hashlib.sha256(archive).hexdigest() == '839e074f8da145e08f82deb358c0cfd74a48afdca4b4d50790299934d8809b1e'
    (p/'scratch/unit-dependency.tar.gz').write_bytes(archive)
    with tarfile.open(fileobj=io.BytesIO(archive)) as t:
        for m in t.getmembers():
            parts=m.name.split('/',1)
            if len(parts)==1 or not parts[1]: continue
            m.name=parts[1]
            t.extract(m,s,filter='data')
    (p/'receipts/unit-dependency-source.json').write_text(json.dumps({'source':'https://api.github.com/repos/cgreen-devs/cgreen/tarball/1.7.0','sha256':hashlib.sha256(archive).hexdigest()},indent=2)+'\n')
for name,args in [
    ('dependency-configure',['cmake','-S',str(s),'-B',str(b),'-DCGREEN_WITH_UNIT_TESTS=OFF','-DCGREEN_WITH_LIBXML2=OFF','-DCGREEN_WITH_DOCS=OFF']),
    ('dependency-build',['make','-C',str(b),'-j16','cgreen_shared'])]:
    r=subprocess.run(['rtk','proxy',*args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=480)
    (p/'scratch/raw'/(name+'.log')).write_bytes(r.stdout)
    (p/'receipts'/(name+'.log')).write_text(r.stdout.decode(errors='replace').replace(str(p),'$PACKET'))
    (p/'receipts'/(name+'.rc')).write_text(str(r.returncode)+'\n')
    print(name, r.returncode, flush=True)
    if r.returncode: raise SystemExit(r.returncode)
