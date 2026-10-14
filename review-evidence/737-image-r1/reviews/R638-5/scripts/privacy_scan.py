#!/usr/bin/env python3
"""Independent privacy scan of an exported OCI image archive.

Usage: privacy_scan.py <image.tar> <out.json> <term> [term ...]
Scans every layer member's bytes, names, link targets and owner metadata, plus the
manifest, config (env, labels, history). Reports counts and member paths only.
"""
import io, json, subprocess, sys, tarfile, hashlib
archive, out, terms = sys.argv[1], sys.argv[2], [t.encode() for t in sys.argv[3:]]
outer = tarfile.open(archive)
def blob(d): return outer.extractfile('blobs/sha256/' + d.split(':', 1)[1]).read()
index = json.loads(outer.extractfile('index.json').read())
mdesc = index['manifests'][0]
manifest = json.loads(blob(mdesc['digest']))
if 'manifests' in manifest:
    manifest = json.loads(blob([m for m in manifest['manifests'] if m.get('platform', {}).get('architecture') == 'amd64'][0]['digest']))
config_bytes = blob(manifest['config']['digest'])
config = json.loads(config_bytes)
report = {'manifest_digest': mdesc['digest'], 'config_digest': manifest['config']['digest'],
          'config_hits': {t.decode(): config_bytes.count(t) for t in terms},
          'history': [h.get('created_by', '') for h in config.get('history', [])],
          'env': config.get('config', {}).get('Env'), 'labels': config.get('config', {}).get('Labels'),
          'user': config.get('config', {}).get('User'), 'layers': []}
for layer in manifest['layers']:
    data = blob(layer['digest'])
    mt = layer['mediaType']
    if 'zstd' in mt:
        data = subprocess.run(['zstd', '-dc'], input=data, capture_output=True, check=True).stdout
    elif 'gzip' in mt:
        import gzip; data = gzip.decompress(data)
    tf = tarfile.open(fileobj=io.BytesIO(data))
    hits = {t.decode(): [] for t in terms}
    owners, mtimes, setuid, count = {}, {}, [], 0
    for m in tf:
        count += 1
        meta = (m.name + '\0' + m.linkname + '\0' + m.uname + '\0' + m.gname).encode()
        body = tf.extractfile(m).read() if m.isfile() else b''
        for t in terms:
            if t in meta or t in body:
                hits[t.decode()].append(m.name)
        owners[f'{m.uid}:{m.gid}:{m.uname}:{m.gname}'] = owners.get(f'{m.uid}:{m.gid}:{m.uname}:{m.gname}', 0) + 1
        mtimes[m.mtime] = mtimes.get(m.mtime, 0) + 1
        if m.mode & 0o6000: setuid.append(m.name)
    report['layers'].append({'digest': layer['digest'], 'diff_sha256': 'sha256:' + hashlib.sha256(data).hexdigest(),
                             'members': count, 'hits': {k: v[:20] for k, v in hits.items() if v},
                             'hit_counts': {k: len(v) for k, v in hits.items() if v},
                             'owners': owners, 'distinct_mtimes': len(mtimes),
                             'top_mtimes': sorted(mtimes.items(), key=lambda kv: -kv[1])[:3], 'setid_members': setuid[:20]})
json.dump(report, open(out, 'w'), indent=1)
print(json.dumps({'layers': [(l['members'], l['hit_counts'], l['distinct_mtimes'], len(l['setid_members'])) for l in report['layers']],
                  'config_hits': {k: v for k, v in report['config_hits'].items() if v}}, indent=None))
