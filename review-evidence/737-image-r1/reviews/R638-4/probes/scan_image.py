#!/usr/bin/env python3
"""R638-4 independent privacy scan of an exported OCI image archive.

Usage: python3 -I scan_image.py <image.tar> <privacy-report.json> <out.json> <clone>/ci/image/privacy.json <local-markers.json>

Reads every layer (gzip or zstd via the zstd CLI), checks member names, link
targets, owner names/ids, PAX headers and file contents for host and identity
markers, and reports each content hit together with whether the builder's
privacy report carries an upstream allowance for that member hash.  Matched
text is never written; only marker labels, paths, hashes and counts.
"""

import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile

ARCHIVE, REPORT, OUT, PRIVACY, LOCAL = sys.argv[1:6]
# Protected identities come from the repository's codepoint table; host,
# account and path markers come from an unpublished local JSON file
# {label: literal}.  Only labels ever reach the output.
MARKERS = {}
for number, rule in enumerate(json.load(open(PRIVACY))['rules']):
    if rule.get('codepoints'):
        text = ''.join(map(chr, rule['codepoints'])).encode()
        MARKERS[f'project-identity-{number}'] = re.compile(rb'(?<![A-Za-z0-9])' + re.escape(text) + rb'(?![A-Za-z0-9])', re.I)
for label, literal in json.load(open(LOCAL)).items():
    MARKERS[label] = re.compile(re.escape(literal.encode()), re.I)


def blob(outer: tarfile.TarFile, digest: str) -> bytes:
    return outer.extractfile('blobs/sha256/' + digest.split(':')[1]).read()


def layer_stream(data: bytes) -> io.BytesIO:
    if data[:4] == b'\x28\xb5\x2f\xfd':
        data = subprocess.run(['zstd', '-dc'], input=data, capture_output=True, check=True).stdout
    elif data[:2] == b'\x1f\x8b':
        import gzip
        data = gzip.decompress(data)
    return io.BytesIO(data)


def allowed_hashes(report: dict) -> set:
    found = set()

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(item, str) and re.fullmatch(r'[0-9a-f]{64}', item) and 'member' in key:
                    found.add(item)
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(report)
    return found


def main() -> int:
    report = json.load(open(REPORT))
    allowed = allowed_hashes(report)
    outer = tarfile.open(ARCHIVE)
    index = json.loads(outer.extractfile('index.json').read())
    manifest = json.loads(blob(outer, index['manifests'][0]['digest']))
    config = blob(outer, manifest['config']['digest'])
    result = {'manifest': index['manifests'][0]['digest'], 'config': manifest['config']['digest'],
              'layers': [], 'config_hits': sorted(k for k, r in MARKERS.items() if r.search(config))}
    for number, layer in enumerate(manifest['layers']):
        stream = layer_stream(blob(outer, layer['digest']))
        rows = {'index': number, 'digest': layer['digest'], 'members': 0, 'owners': set(),
                'metadata_hits': [], 'content_hits': {}}
        with tarfile.open(fileobj=stream) as inner:
            for member in inner:
                rows['members'] += 1
                rows['owners'].add((member.uid, member.gid, member.uname, member.gname))
                meta = ' '.join([member.name, member.linkname or '', member.uname, member.gname,
                                 json.dumps(member.pax_headers)]).encode()
                for key, rx in MARKERS.items():
                    if rx.search(meta):
                        rows['metadata_hits'].append({'marker': key, 'path': member.name})
                if not member.isfile():
                    continue
                data = inner.extractfile(member).read()
                for key, rx in MARKERS.items():
                    if rx.search(data):
                        digest = hashlib.sha256(data).hexdigest()
                        entry = rows['content_hits'].setdefault(key, {'files': 0, 'allowed': 0, 'unallowed': []})
                        entry['files'] += 1
                        if digest in allowed:
                            entry['allowed'] += 1
                        else:
                            entry['unallowed'].append({'path': member.name, 'sha256': digest})
        rows['owners'] = sorted(rows['owners'])
        result['layers'].append(rows)
    json.dump(result, open(OUT, 'w'), indent=1, default=list)
    for rows in result['layers']:
        print(rows['index'], rows['digest'][:19], 'members', rows['members'], 'owners', rows['owners'][:4],
              'meta', len(rows['metadata_hits']),
              {k: (v['files'], v['allowed'], len(v['unallowed'])) for k, v in rows['content_hits'].items()})
    print('config hits', result['config_hits'], 'allowed member hashes', len(allowed))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
