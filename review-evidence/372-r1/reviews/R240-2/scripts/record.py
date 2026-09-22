#!/usr/bin/env python3
"""Run one explicit command through RTK, preserving raw stdout/stderr and exit."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parents[1]
name, *command = sys.argv[1:]
if command[:2] != ['rtk', 'proxy']:
    command = ['rtk', 'proxy', *command]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OUT / 'raw' / (name + '.log')).open('wb') as stream:
    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
receipt = dict(command=command, cwd=os.getcwd(), started=start,
               finished=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               exit=result.returncode)
(OUT / 'raw' / (name + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
sys.exit(result.returncode)
