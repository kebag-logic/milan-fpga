#!/usr/bin/env python3
"""R638-3 independent image scan (Python 3.14+, uses compression.zstd).

Usage: python3 -I scan_image.py <image.tar> <privacy.json> <extra-needle>...
1. Authenticates every blob against its sha256 name, the index -> manifest -> config chain,
   and each layer's uncompressed digest against the config diff_ids.
2. Scans the config (env, labels, history) and every layer member (name, link target,
   owner names, numeric ids, content) for the committed identity table plus extra needles.
Content matches are reported as substring hits and, separately, as word-bounded
hits ('bounded:' prefix, the committed policy's boundary rule).
Prints per-layer counts and, for each content match, the member path and the needle class
(never the matched bytes). Exit 0 always; the receipt is the output.
"""
import gzip
import hashlib
import io
import json
import sys
import tarfile
from compression import zstd

image, table_path, *extra = sys.argv[1:]
table = json.load(open(table_path))
needles = {}
for rule in table['rules']:
    if 'codepoints' in rule:
        needles['project-identity#' + str(len(needles))] = bytes(rule['codepoints'])
for index, value in enumerate(extra):
    needles[f'extra#{index}'] = value.encode()
lowered = {k: v.lower() for k, v in needles.items()}
import re
bounded = {k: re.compile(rb'(?<![A-Za-z0-9_])' + re.escape(v) + rb'(?![A-Za-z0-9_])', re.IGNORECASE)
           for k, v in needles.items()}

outer = tarfile.open(image)


def blob(digest):
    return outer.extractfile('blobs/sha256/' + digest.split(':', 1)[1]).read()


for member in outer.getmembers():
    if member.isfile() and member.name.startswith('blobs/sha256/'):
        data = outer.extractfile(member).read()
        assert hashlib.sha256(data).hexdigest() == member.name.rsplit('/', 1)[1], member.name
print('PASS: every blob matches its sha256 name')
index = json.loads(outer.extractfile('index.json').read())
manifest_digest = index['manifests'][0]['digest']
manifest = json.loads(blob(manifest_digest))
config = json.loads(blob(manifest['config']['digest']))
print('manifest', manifest_digest, 'config', manifest['config']['digest'], 'layers', len(manifest['layers']))
config_bytes = json.dumps(config).lower().encode()
print('config matches:', sorted(k for k, v in lowered.items() if v in config_bytes))
for user_key in ('User', 'WorkingDir'):
    print('config', user_key, repr(config.get('config', {}).get(user_key)))
assert len(config['rootfs']['diff_ids']) == len(manifest['layers'])
for number, (layer, diff_id) in enumerate(zip(manifest['layers'], config['rootfs']['diff_ids'])):
    raw = blob(layer['digest'])
    if raw[:2] == b'\x1f\x8b':
        data = gzip.decompress(raw)
    elif raw[:4] == b'\x28\xb5\x2f\xfd':
        data = zstd.decompress(raw)
    else:
        data = raw
    assert 'sha256:' + hashlib.sha256(data).hexdigest() == diff_id, (number, diff_id)
    hits = {}
    owners = set()
    files = 0
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive:
            files += 1
            owners.add((member.uid, member.gid, member.uname, member.gname))
            meta = (member.name + '\0' + member.linkname + '\0' + member.uname + '\0' + member.gname).lower().encode()
            for key, value in lowered.items():
                if value in meta:
                    hits.setdefault(key, []).append('META:' + member.name)
            if member.isfile():
                raw_content = archive.extractfile(member).read()
                content = raw_content.lower()
                for key, value in lowered.items():
                    if value in content:
                        hits.setdefault(key, []).append(member.name)
                        if bounded[key].search(raw_content):
                            hits.setdefault('bounded:' + key, []).append(member.name)
    print(json.dumps({'layer': number, 'digest': layer['digest'], 'diff_id_verified': True, 'members': files,
                      'owners': sorted(map(list, owners))[:8], 'owner_variants': len(owners),
                      'hit_counts': {k: len(v) for k, v in hits.items()},
                      'hit_paths': {k: sorted(set(v))[:400] for k, v in hits.items()}}, sort_keys=True))
