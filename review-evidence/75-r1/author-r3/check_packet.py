"""Check packet privacy, size, manifests and table receipts before publication.

Usage: python3 check_packet.py REVIEW_HYGIENE_POLICY OUTPUT_DIRECTORY REPOSITORY
The supplied policy stores forbidden names as hashes and is opened read-only.
Wire identifiers are an accepted class under the round-2 decision.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys


def main():
    policy, output, repository = map(Path, sys.argv[1:])
    spec = importlib.util.spec_from_file_location('review_hygiene', policy)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    files = sorted(p for p in output.rglob('*') if p.is_file())
    files += [repository/'docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md',
              repository/'docs/findings/README.md']
    problems = []
    for path in files:
        label = str(path.relative_to(output)) if path.is_relative_to(output) else str(path.relative_to(repository))
        if path.is_symlink() or path.stat().st_size > 200_000:
            problems.append([label, 'symlink or oversized file'])
        source = path.read_text()
        words = set(re.findall(r'[a-z0-9][a-z0-9-]*', source.lower()))
        for category, digests in module.NAME_HASHES.items():
            if any(hashlib.sha256(word.encode()).hexdigest()[:16] in digests for word in words):
                problems.append([label, category])
        variables = re.findall(r'\$\{?([A-Za-z_][A-Za-z0-9_]*)', source)
        for category, digests in module.VAR_HASHES.items():
            if any(hashlib.sha256(word.encode()).hexdigest()[:16] in digests for word in variables):
                problems.append([label, category])
        for category in ('abs-or-tmp-path', 'serial-word'):
            if re.search(module.PATTERNS[category], source):
                problems.append([label, category])
    receipts = json.loads((output/'table-render-check.json').read_text())
    for receipt in receipts:
        name = receipt['file']
        path = output/name.removeprefix('addendum/') if name.startswith('addendum/') else repository/name
        if hashlib.sha256(path.read_bytes()).hexdigest() != receipt['sha256']:
            problems.append([name, 'rendered content changed'])
    rendered = {r['file'].removeprefix('addendum/') for r in receipts}
    for path in output.rglob('*.md'):
        if str(path.relative_to(output)) not in rendered:
            problems.append([str(path.relative_to(output)), 'Markdown not render-checked'])
    for path in output.glob('talker-*/MANIFEST.sha256'):
        for line in path.read_text().splitlines():
            digest, name = line.split('  ', 1)
            if hashlib.sha256((path.parent/name).read_bytes()).hexdigest() != digest:
                problems.append([str(path.relative_to(output)), 'cycle manifest mismatch'])
    result = dict(result='FAIL' if problems else 'PASS', files_checked=len(files),
                  maximum_packet_file_bytes=max(p.stat().st_size for p in output.rglob('*') if p.is_file()),
                  policy_sha256=hashlib.sha256(policy.read_bytes()).hexdigest(),
                  accepted_class='wire identifiers as in round-2 decision',
                  rendered_tables=sum(len(r['tables']) for r in receipts),
                  rendered_body_rows=sum(t['body_rows'] for r in receipts for t in r['tables']),
                  problems=problems)
    (output/'packet-check.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
