#!/usr/bin/env python3
"""Check that grouped builder evidence covers the __main__ loop exactly once.

Usage: python3 -I builder_groups_cover.py <clone>/sw/builder/test_builder.py <dir with builder-functions-*.json>
"""
import ast
import collections
import hashlib
import json
import pathlib
import sys

src = pathlib.Path(sys.argv[1])
tree = ast.parse(src.read_text())
loop = None
for node in ast.walk(tree):
    if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == 'fn' \
            and isinstance(node.iter, ast.Tuple):
        loop = node
        break
names = [e.id for e in loop.iter.elts]
sha = hashlib.sha256(src.read_bytes()).hexdigest()
ran = collections.Counter()
hashes = set()
for path in sorted(pathlib.Path(sys.argv[2]).glob('builder-functions-*.json')):
    record = json.loads(path.read_text())
    hashes.add(record['source_sha256'])
    ran.update(r['name'] for r in record['results'])
    assert record['require_rv32'] is True, path
expected = collections.Counter(names)
print('loop invocations', len(names), 'source sha256', sha)
print('evidence hashes', sorted(hashes))
print('recorded results', sum(ran.values()))
print('missing', sorted((expected - ran).elements()))
print('extra', sorted((ran - expected).elements()))
print('duplicates', sorted(n for n, c in ran.items() if c > 1))
print('EXACT COVER' if ran == expected and hashes == {sha} else 'NOT EXACT')
