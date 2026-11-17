#!/usr/bin/env python3
"""Render both changed workflow diagrams in a bounded foreground process."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root, out = map(Path, sys.argv[1:3])
blocks = re.findall(r'```mermaid\n(.*?)```', (root/'CONTRIBUTING.md').read_text(), re.S)
assert len(blocks) == 2
version = subprocess.check_output(['mmdc','--version'],text=True).strip()
def render(i):
    source = out/'scratch'/f'diagram-{i}.mmd'
    source.write_text(blocks[i])
    commands = []
    for ext in ['svg','png']:
        dest = out/f'diagram-{i}.{ext}'
        cmd = ['mmdc','-j','1','-w','3600','-i',str(source),'-o',str(dest)]
        p = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        commands.append(dict(format=ext,rc=p.returncode,output=p.stdout,sha256=hashlib.sha256(dest.read_bytes()).hexdigest() if dest.exists() else None))
        assert p.returncode == 0, p.stdout
    return dict(block=i,source_sha256=hashlib.sha256(blocks[i].encode()).hexdigest(),commands=commands)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    rows=list(pool.map(render,range(2)))
print(json.dumps(dict(renderer_version=version,results=rows),indent=2))
