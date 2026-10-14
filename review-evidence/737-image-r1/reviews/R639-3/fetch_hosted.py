#!/usr/bin/env python3
"""Retrieve only the named hosted execution and its pinned runner manifest."""
from pathlib import Path
import subprocess
import urllib.request
packet=Path(__file__).resolve().parent
scratch=packet/'scratch'; scratch.mkdir(exist_ok=True)
for suffix,name in (('', 'hosted-job.json'),('/logs','hosted-docs.log')):
    args=['gh','api','repos/kebag-logic/milan-fpga/actions/jobs/115696619496'+suffix]
    if suffix:args.append('--allow-escape-sequences')
    result=subprocess.run(args,check=True,capture_output=True)
    (scratch/name).write_bytes(result.stdout)
url='https://raw.githubusercontent.com/actions/runner-images/ubuntu24/20261004.327/images/ubuntu/Ubuntu2404-Readme.md'
with urllib.request.urlopen(url,timeout=60) as stream:
    (scratch/'runner-manifest.md').write_bytes(stream.read())
print('Retrieved the assigned current-dev docs job and pinned runner manifest.')
