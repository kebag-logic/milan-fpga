"""A regradeable extract of the 4x4 link-rate census (census 4): for each variant, its build.json, each case's log
cut to the lines the 100 Mb/s grade reads (egress_mii.parse: EGRESSQ, TXREADY, TXC, WIRE and EGRESS, each kept
whole and in order), and the run's group grades and results.json, which the held-egress ledger reads.
FILES.json maps every file written to its source's size and sha256. usage: extract5.py C4Q OUT"""
import hashlib, json, shutil, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
assert not out.exists(), out
KINDS = ('EGRESSQ ', 'TXREADY ', 'TXC ', 'WIRE ', 'EGRESS ')
files = {}
def note(dest, source, data):
    files[str(dest.relative_to(out))] = dict(source=str(source.relative_to(src)), source_bytes=source.stat().st_size,
                                             source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                             bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
for variant in sorted(p for p in src.iterdir() if (p / 'build.json').exists()):
    v = out / variant.name; (v / 'results').mkdir(parents=True)
    for name in ['build.json']:
        data = (variant / name).read_bytes(); (v / name).write_bytes(data); note(v / name, variant / name, data)
    for f in sorted((variant / 'results').iterdir()):
        if f.suffix == '.log':
            lines = [l for l in f.read_text(errors='strict').splitlines(keepends=True) if l.startswith(KINDS)]
            data = ''.join(lines).encode()
        elif f.suffix == '.json':
            data = f.read_bytes()
        else:
            continue
        dest = v / 'results' / f.name; dest.write_bytes(data); note(dest, f, data)
(out / 'FILES.json').write_text(json.dumps(files, indent=1, sort_keys=True) + '\n')
print('EXTRACT', len(files), 'files', sum(r['bytes'] for r in files.values()), 'bytes')
