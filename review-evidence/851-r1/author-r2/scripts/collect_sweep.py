"""collect_sweep.py <sweep-dir> <dest>: each shard's spec, summary, results and suite logs, masked. A log over 200 KB is
kept as its last 80 lines, with its SHA-256 and size in <dest>/RAW-RECORDS.txt."""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mask import mask

src, dest = Path(sys.argv[1]), Path(sys.argv[2])
raw = []
for shard in sorted(src.glob('shard-*')):
    out = dest / shard.name
    out.mkdir(parents=True, exist_ok=True)
    files = [shard / 'spec.json', shard / 'spec' / '01.log', shard / 'spec' / 'results.json']
    files += sorted(p for p in (shard / 'logs').rglob('*') if p.is_file())
    for p in files:
        if not p.exists():
            continue
        data = p.read_bytes()
        rel = p.relative_to(shard).as_posix().replace('/', '__')
        text = mask(data.decode(errors='replace'))
        if len(text.encode()) > 200 * 1024:
            raw.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {shard.name}/{rel}')
            (out / (rel + '.tail')).write_text(''.join(text.splitlines(True)[-80:]))
        else:
            (out / rel).write_text(text)
(dest / 'RAW-RECORDS.txt').write_text('\n'.join(raw) + '\n')
print(len(raw), 'large logs recorded by digest')
