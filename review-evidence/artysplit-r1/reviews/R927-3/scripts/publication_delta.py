"""Compare the published census extract with the author's inventory and the publisher's MANIFEST.json.
usage: python3 -I publication_delta.py RECEIPTS_DIR TOP_MANIFEST_JSON
Prints, per altered file, whether the inventory hash equals the publisher's original_sha256 and the on-disk hash
equals its published_sha256, and the affected cases."""
import hashlib, json, sys
from pathlib import Path
root, top = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
inv = {p: h for p, _, h in (l.split('\t') for l in (root / 'FILES.tsv.part0001.txt').read_text().splitlines()[1:])}
pub = {e['file'].split('author-r8/receipts/', 1)[1]: e for e in top if e['file'].startswith('author-r8/receipts/')}
cases, n = set(), 0
for path, digest in sorted(inv.items()):
    disk = hashlib.sha256((root / path).read_bytes()).hexdigest()
    if disk == digest:
        continue
    e = pub.get(path, {})
    n += 1
    cases.add('/'.join(path.split('/')[2:4]))
    print(f'ALTERED {path} inventory==publisher.original:{e.get("original_sha256") == digest} '
          f'disk==publisher.published:{e.get("published_sha256") == disk} path_redacted:{e.get("path_redacted")}')
print(f'RESULT altered_files={n} affected_cases={len(cases)}')
for c in sorted(cases):
    print('CASE', c)
