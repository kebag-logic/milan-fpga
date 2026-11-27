"""Disposable probe: a copy of a census extract whose case manifests and census rows are re-bound to the bytes
on disk (data files hard-linked), optionally without some cases. It answers whether the on-disk bytes still
grade as recorded; it is not evidence of provenance. usage: python3 -I rebind_probe.py EXTRACT OUT [DROP_CASE...]"""
import hashlib, json, os, sys
from pathlib import Path
src, out, drop = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), set(sys.argv[3:])
sha = lambda b: hashlib.sha256(b).hexdigest()
census = json.loads((src / 'census.json').read_text())
rows, rebound = [], 0
for row in census['cases']:
    if row['case'] in drop:
        continue
    sd, od = (src / row['manifest']).parent, (out / row['manifest']).parent
    od.mkdir(parents=True, exist_ok=True)
    for f in sd.iterdir():
        if f.name != 'manifest.json':
            os.link(f, od / f.name)
    m = json.loads((sd / 'manifest.json').read_text())
    whole = b''
    for p in m['extract']['parts']:
        data = (sd / p['file']).read_bytes(); whole += data
        if sha(data) != p['sha256']:
            p['sha256'] = sha(data); rebound += 1
    m['extract']['sha256'] = sha(whole)
    text = json.dumps(m, separators=(',', ':')) + '\n'
    (od / 'manifest.json').write_text(text)
    rows.append(dict(row, sha256=sha(text.encode())))
os.link(src / "published-qualification.json", out / "published-qualification.json")
(out / 'census.json').write_text(json.dumps(dict(census, cases=rows), indent=1) + '\n')
print(f'PROBE cases={len(rows)} rebound_parts={rebound} dropped={sorted(drop)}')
