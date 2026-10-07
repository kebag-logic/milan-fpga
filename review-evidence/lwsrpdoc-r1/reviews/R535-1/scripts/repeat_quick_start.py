#!/usr/bin/env python3
"""Run the second occurrences of the four shared quick-start commands.

Usage: python3 scripts/repeat_quick_start.py PACKET
"""
import json
import os
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
source = packet / "scratch/command-source"
prefix = packet / "scratch/dependency-prefix"
env = os.environ.copy()
env.update(CPATH=str(prefix / "include"), LIBRARY_PATH=str(prefix / "lib"),
           LD_LIBRARY_PATH=str(prefix / "lib"), CMAKE_PREFIX_PATH=str(prefix), PYTHONDONTWRITEBYTECODE="1")
commands = (source / "README.md").read_text().split("~~~sh\n")[1].split("~~~")[0].splitlines()
records = []
for line, command in enumerate(commands, 35):
    result = subprocess.run(["bash", "-c", command], cwd=source, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    name = "quick-start-" + str(line)
    output = result.stdout.replace(str(source), "<source>").replace(str(packet), "<packet>")
    (packet / "receipts" / (name + ".log")).write_text(output)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    records.append(dict(page="README.md", line=line, command=command, rc=result.returncode))
(packet / "receipts/quick-start-commands.json").write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps(records, indent=2))
