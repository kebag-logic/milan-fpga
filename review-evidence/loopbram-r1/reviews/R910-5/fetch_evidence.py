#!/usr/bin/env python3
"""Fetch a bounded public receipt selection and verify published SHA256s."""
import concurrent.futures
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
REF = 'e55f3f332e8b629a5f933ff3908492ec2e72975a'
PREFIX = 'review-evidence/loopbram-r1/'

def fetch(path):
    return subprocess.check_output(['gh', 'api', f'repos/kebag-logic/milan-fpga/contents/{PREFIX}{path}?ref={REF}', '-H', 'Accept: application/vnd.github.raw+json'])

def wanted(path):
    if path.startswith('author-r6b/'):
        return True
    if not path.startswith('author-r8/'):
        return False
    name = pathlib.PurePosixPath(path).name
    return (name in {'REVIEW-READY.md', 'HANDOFF-r8.md', 'PR-BODY.md', 'source-binding.json.txt', 'route-summary.json.txt', 'firmware-memory.json.txt', 'inputs-endstation_ax7101_1x1_tdm8.json.txt', 'inputs-endstation_ax7101_8x8.json.txt', 'identity-prepare.json.txt', 'generated-hex.start.txt.txt', 'generated-hex.end.txt.txt', 'route-outputs-sha256.json.txt', 'ordinary--endstation_ax7101_8x8--export.log.txt'} or name.endswith(('signoff_grade.txt.txt', 'route_status.rpt.txt', 'routed_util.rpt.txt', 'timing.rpt.part001.txt', 'measure_route.tcl.txt')))

def main():
    raw = fetch('MANIFEST.json')
    manifest = json.loads(raw)
    target = ROOT / 'scratch' / 'public'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'MANIFEST.json').write_bytes(raw)
    selected = [r for r in manifest if wanted(r['file'])]
    def one(row):
        data = fetch(row['file'])
        path = target / row['file']
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        actual = hashlib.sha256(data).hexdigest()
        assert actual == row['published_sha256'], row['file']
        return {'path': row['file'], 'bytes': len(data), 'sha256': actual, 'match': True}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(one, selected))
    result = {'ref': REF, 'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'files': results, 'verified': len(results), 'signature_claim': 'SHA256 manifest integrity only; no detached signature supplied by this manifest.'}
    (ROOT / 'evidence-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'PASS: {len(results)} selected public receipts match the published manifest')

if __name__ == '__main__':
    main()
