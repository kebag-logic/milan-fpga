"""Export exact pinned sources for R221 probes; no changes to the review clone."""
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile

source = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
pins = {'protocol-processor': '424c688fa2205b934a7689a58f2aa766420f2326',
        'gptp-processor': 'c1b617435824929a790739ea8585c3fe1a328cc0',
        'third_party/verilog-axis': '48ff7a7e2ef782cf778d47910cf85835c64b1bce'}


def export(repo, ref, destination):
    data = subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(repo), 'archive', ref],
        env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'})
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(destination, filter='data')


for name, ref in [('candidate', 'd81a302760b84f32d2aa019643f57682bb6e052c'),
                  ('original-base', 'b17580b91deb11f3441dfc5d7f9fafe539d929b8')]:
    destination = output / 'scratch' / name
    if destination.exists():
        raise SystemExit('Use a fresh output directory; refusing to overwrite scratch')
    export(source, ref, destination)
    for submodule, pin in pins.items():
        export(source / submodule, pin, destination / submodule)
    print(name, ref)
