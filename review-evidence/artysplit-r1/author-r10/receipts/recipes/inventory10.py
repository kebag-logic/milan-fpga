"""FILES inventory of a packet: every file's bytes and SHA256 as numbered FILES.tsv parts with a manifest."""
import hashlib, json, sys
from pathlib import Path
OUT = Path(sys.argv[1])
files = sorted(p for p in OUT.rglob('*') if p.is_file() and not p.name.startswith('FILES.') and p.name != 'INDEX.md')
rows = [f'{p.relative_to(OUT)}\t{p.stat().st_size}\t{hashlib.sha256(p.read_bytes()).hexdigest()}' for p in files]
data = ('path\tbytes\tsha256\n' + '\n'.join(rows) + '\n').encode()
pieces, start = [], 0
while start < len(data):
    end = min(start + 180_000, len(data))
    if end < len(data):
        end = data.rfind(b'\n', start, end) + 1
    name = f'FILES.tsv.part{len(pieces) + 1:04d}.txt'
    (OUT / name).write_bytes(data[start:end])
    pieces.append(dict(file=name, bytes=end - start, sha256=hashlib.sha256(data[start:end]).hexdigest()))
    start = end
(OUT / 'FILES.manifest.json').write_text(json.dumps(dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                                                         parts=pieces), indent=1) + '\n')
print('INVENTORY', len(files))
