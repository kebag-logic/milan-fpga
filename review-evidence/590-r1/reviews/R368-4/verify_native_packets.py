#!/usr/bin/env python3
"""Verify the published native-evidence packets and compare merge-dev with round 3.

Usage: verify_native_packets.py <evidence 590-r1 dir> <repo at exact head> <out.json>
For every artifact of each packet's native-artifacts.json, locate its bytes
(stored file, gzip, or the uncompressed copy under raw/ or native-evidence-raw/)
and check raw size and SHA-256. Then pair merge-dev and round-3 artifacts by
name and report which raw bytes are identical and which differ.
"""
import gzip, hashlib, json, sys
from pathlib import Path

base, repo, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PACKS = {'mergedev': base / 'author-mergedev', 'r3': base / 'author-r3'}
RAWDIRS = {'mergedev': ['raw'], 'r3': ['native-evidence-raw', 'raw']}

MAN = {e['file']: e for e in json.loads((base.parent.parent / 'MANIFEST.json').read_text())}
REDACTED = []

def locate(pack, key, art):
    for s in art['stored']:
        p = pack / s['path']
        if p.is_file():
            data = p.read_bytes()
            if hashlib.sha256(data).hexdigest() != s['sha256'] or len(data) != s['size']:
                # The publisher redacts local paths; accept only a manifest entry
                # binding the original hash to these exact published bytes.
                e = MAN.get(str(p.relative_to(base.parent.parent)))
                if (e and e['path_redacted'] and e['original_sha256'] == s['sha256']
                        and e['published_sha256'] == hashlib.sha256(data).hexdigest()):
                    REDACTED.append((key, art['name']))
                    return 'REDACTED', s['path']
                return None, 'stored hash/size mismatch ' + s['path']
            return (gzip.decompress(data) if p.suffix == '.gz' else data), s['path']
        rel = s['path'][:-3] if s['path'].endswith('.gz') else s['path']
        for rd in RAWDIRS[key]:
            for cand in (pack / rd / rel, pack / rd / Path(rel).name):
                if cand.is_file():
                    return cand.read_bytes(), str(cand.relative_to(pack))
    return None, 'missing'

result, bad = {}, []
for key, pack in PACKS.items():
    arts = json.loads((pack / 'native-artifacts.json').read_text())
    res = {}
    for a in arts:
        data, where = locate(pack, key, a)
        red = data == 'REDACTED'
        ok = red or (data is not None and len(data) == a['raw_size'] and hashlib.sha256(data).hexdigest() == a['raw_sha256'])
        res[a['name']] = dict(ok=ok, redacted=red, where=where, raw_sha256=a['raw_sha256'])
        if not ok:
            bad.append((key, a['name'], where))
    result[key] = res
    print(f"{key}: {sum(v['ok'] for v in res.values())}/{len(res)} artifacts verified "
          f"({sum(v['redacted'] for v in res.values())} via manifest-bound path redaction)")
for b in bad:
    print('UNVERIFIED', b)

def norm(n):
    return n[:-3] if n.endswith('.gz') else n
md = {norm(k): v for k, v in result['mergedev'].items()}
r3 = {norm(k): v for k, v in result['r3'].items()}
same = sorted(n for n in md if n in r3 and md[n]['raw_sha256'] == r3[n]['raw_sha256'])
diff = sorted(n for n in md if n in r3 and md[n]['raw_sha256'] != r3[n]['raw_sha256'])
print('paired identical:', len(same)); print('paired different:', len(diff))
for n in diff:
    print('  DIFF', n)
json.dump(dict(verify=result, unverified=bad, identical=same, different=diff,
               only_mergedev=sorted(set(md) - set(r3)), only_r3=sorted(set(r3) - set(md))),
          open(out, 'w'), indent=1)
sys.exit(1 if bad else 0)
