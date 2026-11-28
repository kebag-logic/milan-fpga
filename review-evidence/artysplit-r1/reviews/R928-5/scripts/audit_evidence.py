#!/usr/bin/env python3
"""Verify the published round-10 and round-11 author packets against their outer and inner integrity records.

usage: python3 -I audit_evidence.py EVIDENCE_ROOT
"""
import hashlib
import json
import sys
from pathlib import Path


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main(root: Path) -> int:
    outer = json.loads((root / 'MANIFEST.json').read_text())
    for tag in ('author-r10', 'author-r11'):
        rows = [r for r in outer if r['file'].startswith(tag + '/')]
        on_disk = sorted(str(p.relative_to(root)) for p in (root / tag).rglob('*') if p.is_file())
        assert sorted(r['file'] for r in rows) == on_disk, (tag, len(rows), len(on_disk))
        changed = []
        for r in rows:
            assert sha(root / r['file']) == r['published_sha256'], r['file']
            if r['original_sha256'] != r['published_sha256'] or r['path_redacted']:
                changed.append(r['file'])
        print(f'PASS outer {tag}: {len(rows)} files, published == actual; transformed by publication: {changed}')
    extract_rows = [r for r in outer if r['file'].startswith('author-r10/receipts/census-extract/')]
    assert all(r['original_sha256'] == r['published_sha256'] and not r['path_redacted'] for r in extract_rows)
    print(f'PASS outer census-extract: {len(extract_rows)} files original == published == actual, none redacted')
    for tag in ('author-r10', 'author-r11'):
        receipts = root / tag / 'receipts'
        inner = json.loads((receipts / 'MANIFEST.json').read_text())
        for r in inner:
            path = receipts / r['path']
            assert path.stat().st_size == r['bytes'] and sha(path) == r['sha256'], r['path']
        scrubbed = [r['path'] for r in inner if r['original_sha256'] != r['sha256']]
        print(f'PASS inner {tag}/receipts/MANIFEST.json: {len(inner)} files bytes and SHA256; scrub-changed: {scrubbed}')
    extract = root / 'author-r10/receipts/census-extract'
    files = json.loads((extract / 'FILES.json').read_text())
    for r in files:
        assert sha(extract / r['path']) == r['sha256'], r['path']
    listed = {r['path'] for r in files}
    present = {str(p.relative_to(extract)) for p in extract.rglob('*') if p.is_file()}
    print(f'PASS extract FILES.json: {len(files)} entries; files present {len(present)}; '
          f'outside the inventory: {sorted(present - listed)}; listed but absent: {sorted(listed - present)}')
    census = json.loads((extract / 'census.json').read_text())
    for r in census['cases']:
        assert sha(extract / r['manifest']) == r['sha256'], r['case']
    sizes = sorted((p.stat().st_size, str(p.relative_to(extract))) for p in extract.rglob('*') if p.is_file())
    print(f'PASS census.json: {len(census["cases"])} manifests; source_head={census["source_head"]} '
          f'part_limit={census["part_limit"]}')
    print(f'TOTAL {sum(s for s, _ in sizes)} bytes; largest {sizes[-1]}')
    print('QUALIFICATION SHA256', sha(extract / 'published-qualification.json'))
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
