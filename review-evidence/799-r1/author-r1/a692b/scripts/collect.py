"""collect.py <src-dir> <dest-dir>: copy a gate's result files into the receipts, host paths replaced by
placeholders; a file over 150 KB is recorded by sha256 and size instead (`<name>.sha256-size`)."""
import hashlib
import re
import sys
from pathlib import Path

src, dest = Path(sys.argv[1]), Path(sys.argv[2])
dest.mkdir(parents=True, exist_ok=True)
SUBS = [(re.compile(r'$VALIDATION_STORAGE/scratch/799-a692b'), '<scratch>'), (re.compile(r'$LANES/799-a692b-shard\d'), '<shard-clone>'),
        (re.compile(r'$LANES/799-adopt6'), '<lane>'), (re.compile(r'$VALIDATION_STORAGE/a692b'), '<tmp>'),
        (re.compile(r'$VALIDATION_TOOLS'), '<tools>'), (re.compile(r'$VALIDATION_STORAGE/scratch/a662'), '<tools>/a662'),
        (re.compile(r'$WORKSPACE_HOME/Xilinx'), '<vivado>'), (re.compile(r'$WORKSPACE_HOME'), '<home>'), (re.compile(r'$VALIDATION_STORAGE'), '<data>')]
for path in sorted(p for p in src.rglob('*') if p.is_file()):
    rel = path.relative_to(src)
    out = dest / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    data = path.read_bytes()
    if len(data) > 150_000:
        (out.parent / (out.name + '.sha256-size')).write_text(f'{hashlib.sha256(data).hexdigest()}  {len(data)} bytes  {rel}\n')
        continue
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        (out.parent / (out.name + '.sha256-size')).write_text(f'{hashlib.sha256(data).hexdigest()}  {len(data)} bytes  {rel}\n')
        continue
    for pat, rep in SUBS:
        text = pat.sub(rep, text)
    out.write_text(text)
print('collected', src, '->', dest)
