#!/usr/bin/env python3
"""Fetch only published author evidence and verify its manifest."""
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
REF = 'd46de11e7b5e590a914a9f86718477c6b203fbab'
REPO = 'kebag-logic/milan-fpga'

def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPO}/{path}']))

def fetch(path):
    data = api(f'contents/{path}?ref={REF}')
    return base64.b64decode(data['content'])

def main():
    dest = OUT / 'scratch' / 'public'
    dest.mkdir(parents=True, exist_ok=True)
    result = {'publication_commit': REF, 'rounds': {}}
    for rnd in ('adpcdl-r1', 'adpcdl-r2'):
        prefix = 'review-evidence/' + rnd
        manifest = fetch(prefix + '/MANIFEST.json')
        entries = [x for x in json.loads(manifest) if x['file'].startswith('author/')]
        (dest / rnd).mkdir(exist_ok=True)
        (dest / rnd / 'MANIFEST.json').write_bytes(manifest)
        def one(entry):
            data = fetch(prefix + '/' + entry['file'])
            p = dest / rnd / entry['file']
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            digest = hashlib.sha256(data).hexdigest()
            assert digest == entry['published_sha256'], entry['file']
            # Report locations only, never repeat potentially private text.
            hits = [n for n, line in enumerate(data.decode(errors='replace').splitlines(), 1)
                    if re.search(r'/(?:home|srv|data|mnt|media|Users)/', line)]
            return {'file': entry['file'], 'sha256': digest, 'matches': True,
                    'host_path_lines': hits}
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            result['rounds'][rnd] = list(pool.map(one, entries))
    verification = api('commits/' + REF)['commit']['verification']
    result['signature'] = {k: verification[k] for k in ('verified', 'reason')}
    (OUT / 'public-packet-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'files_verified': {k: len(v) for k,v in result['rounds'].items()},
                      'signature': result['signature'],
                      'round_two_host_path_hits': sum(bool(x['host_path_lines']) for x in result['rounds']['adpcdl-r2'])}))

if __name__ == '__main__':
    main()
