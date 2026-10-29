"""collect_mutants.py <scratch-mut-dir> <receipts-dir>: copy each mutant stream's verdicts into the receipts, with the
SHA-256 and size of every log (not the logs), and the lines each log printed that the verdicts rest on (FAIL lines,
the cut and #207 diagnostics, the check tallies). Host paths are removed from copied text."""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
KEEP = re.compile(r'^\s*(FAIL\b|\[FAIL\]|\[cut\]|\[#207\]|\d+ checks:)')
for stream in sorted(p for p in src.iterdir() if p.is_dir()):
    out = dst / stream.name
    out.mkdir(parents=True, exist_ok=True)
    digests, lines = [], []
    for f in sorted(stream.iterdir()):
        if f.suffix == '.log':
            data = f.read_bytes()
            digests.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {f.name}')
            kept = [l for l in data.decode(errors='replace').splitlines() if KEEP.match(l)]
            lines.append(f'## {f.name}\n' + '\n'.join(kept))
        elif f.name in ('results.json', 'stream.out', 'stream.rc', 'start', 'end'):
            text = f.read_text().replace(str(src.parent), '<scratch>')
            (out / f.name).write_text(text)
    (out / 'logs.sha256').write_text('\n'.join(digests) + '\n')
    (out / 'log-lines.txt').write_text('\n\n'.join(lines) + '\n')
    print(stream.name, len(digests), 'logs')
