#!/usr/bin/env python3
"""Run documentation, diagram and interface checks on a disposable archive."""
import io
import pathlib
import subprocess
import sys
import tarfile

packet = pathlib.Path(__file__).resolve().parent
source = pathlib.Path(sys.argv[1]).resolve()
dest = packet / 'scratch' / 'docs-check'
dest.mkdir(parents=True, exist_ok=True)
archive = subprocess.check_output(['git', 'archive', '2022d363fc622f6bbf4c312239fc3db741b4d29a'], cwd=source)
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(dest, filter='data')
run = subprocess.run(['make', '-j16', 'docs', 'contract'], cwd=dest,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(packet / 'docs-contract.log').write_bytes(run.stdout)
(packet / 'docs-contract.rc').write_text(str(run.returncode) + '\n')
print(run.stdout.decode(), end='')
raise SystemExit(run.returncode)
