"""collect_gates.py <gates-dir> <dest>: every gate log and rc of each group, masked; a log over 200 KB is kept as its
last 80 lines with its SHA-256 and size in <dest>/RAW-RECORDS.txt."""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mask import mask

src, dest = Path(sys.argv[1]), Path(sys.argv[2])
raw = []
for p in sorted(q for q in src.rglob('*') if q.is_file()):
    rel = p.relative_to(src)
    out = dest / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    data = p.read_bytes()
    text = mask(data.decode(errors='replace'))
    if len(text.encode()) > 200 * 1024:
        raw.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel.as_posix()}')
        out.with_name(out.name + '.tail').write_text(''.join(text.splitlines(True)[-80:]))
    else:
        out.write_text(text)
(dest / 'RAW-RECORDS.txt').write_text('\n'.join(raw) + '\n')
print(len(raw), 'large logs recorded by digest')
