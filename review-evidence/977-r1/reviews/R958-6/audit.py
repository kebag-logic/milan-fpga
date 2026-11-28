#!/usr/bin/env python3
"""Audit the public packet and narrow delta; run from the exact candidate clone."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
REF = 'd963a0c0697795b4ad4f6247b7379bf5cddd81ad'
PREFIX = 'review-evidence/977-r1/'
HEAD = 'a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35'

def git(*args):
    return subprocess.check_output(['git', *args])

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def published(name):
    data = git('show', REF + ':' + PREFIX + name)
    expected = manifest[name]['published_sha256']
    actual = hashlib.sha256(data).hexdigest()
    assert actual == expected, name
    verified.append({'path': name, 'bytes': len(data), 'sha256': actual})
    return data

def maps(data):
    result = {}
    section = None
    for line in data.decode().splitlines():
        if line.startswith('## '):
            section = line[3:]
            result[section] = {}
        m = re.fullmatch(r'([0-9a-f]{64})  (.+\.elf)', line)
        if m:
            assert m[2] not in result[section]
            result[section][m[2]] = m[1]
    return {k: v for k, v in result.items() if v}

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
manifest = {x['file']: x for x in json.loads(git('show', REF + ':' + PREFIX + 'MANIFEST.json'))}
verified = []
for name in manifest:
    if name.startswith('author-r14/') and 'HANDOFF' not in name:
        published(name)
identity = maps(published('author-r14/receipts/elf-identity-a5b19f70.txt'))
old = maps(published('author-r10/receipts/r10d/elf-identity-final.txt'))
assert set(identity) == {'a5b19f70', '25ff0632'}
assert len(identity['a5b19f70']) == len(identity['25ff0632']) == 80
assert identity['a5b19f70'] == identity['25ff0632'] == old['25ff0632'] == old['e59cf6ea']
save('elf-identity-audit.json', {'equal_pairs': 80, 'baseline': '25ff0632',
    'independent_older_receipt_matches': True, 'measured_image_baseline': 'e59cf6ea',
    'limit': 'Published SHA-256 build receipts verified; ELF binaries were not available or rebuilt.',
    'paths': identity['a5b19f70']})
notes = []
for round_ in ('author-r10', 'author-r11'):
    name = round_ + '/receipts/SUPERSESSION-NOTE.md'
    data = published(name)
    target = OUT / 'public' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    assert git('show', '63ebbbacee3d6c366274d0b756f86433a7588a30:' + PREFIX + name) == data
    targets = re.findall(r'^\| `[^`]+\.gz` \| `([^`]+)` \|$', data.decode(), re.M)
    for path in targets:
        published(round_ + '/receipts/' + path)
    notes.append({'note': name, 'mapped_paths_verified': len(targets), 'linked_commit_bytes_match': True})
save('supersession-links.json', notes)
save('packet-integrity.json', {'evidence_commit': REF, 'verified': verified})

class WithoutDocs(ast.NodeTransformer):
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return None
        return self.generic_visit(node)

def code(data):
    return ast.dump(WithoutDocs().visit(ast.parse(data)), include_attributes=False)

delta = {}
for base in ('4461d77c', '3256d1d2'):
    names = git('diff', '--name-only', base, HEAD).decode().splitlines()
    assert not any(n.startswith(('sw/', 'hdl/', 'third_party/')) for n in names)
    modules = {}
    for name in names:
        if name.endswith('.py'):
            modules[name] = code(git('show', base + ':' + name)) == code(git('show', HEAD + ':' + name))
            assert modules[name], name
    delta[base] = {'files': names, 'equal_executable_ast_excluding_docstrings': modules,
        'history': git('log', '--format=%H %s', base + '..' + HEAD).decode().splitlines()}
assert len(delta['4461d77c']['files']) == 4
assert len(delta['3256d1d2']['files']) == 5
save('delta-audit.json', delta)
docs = (OUT / 'public/author-r14/receipts/docs/docs-steps-a5b19f70.txt').read_text()
rows = re.findall(r'^(\d\d)-.*?rc=(\d+)', docs, re.M)
assert len(rows) == 100 and all(rc == '0' for _, rc in rows)
pr = json.loads((OUT / 'pr.json').read_text())['body']
assert 'the historical index notes are published beside the round-10 and round-11 receipt indexes' in pr
assert 'historical index notes remain to be published' not in pr
for n in (10, 11):
    assert ('63ebbbacee3d6c366274d0b756f86433a7588a30/' + PREFIX +
            f'author-r{n}/receipts/SUPERSESSION-NOTE.md') in pr
for name, line in [('docs/reference/FR_NFR.md', 427), ('docs/design/SPLIT_CONTROL_MEMORY.md', 2548)]:
    text = Path(name).read_text().splitlines()[line - 1]
    assert 'issuecomment-7235670586' in text and '0.79' in text
docs_result = {'docs_steps': 100, 'all_rc_zero': True, 'inventory_parity_skip_in_no_git_fixture': True,
    'publication_wording_resolved': True, 'linked_notes': 2, 'authority_links_at_required_lines': True}
for base in ['origin/dev-soft-core', '4461d77c', '3256d1d2']:
    check = subprocess.run(['git', 'diff', '--check', base + '..HEAD'], capture_output=True, text=True)
    assert check.returncode == 0
    docs_result['whitespace_' + base] = {'rc': check.returncode, 'stdout': check.stdout, 'stderr': check.stderr}
added = [x[1:] for x in git('diff', '4461d77c', HEAD, '--', '*.py').decode().splitlines()
         if x.startswith('+') and not x.startswith('+++')]
assert not any(re.search(r'issuecomment-\d|comment \d{8,}|\[R\d|\bB\d+\b|decision pending', x) for x in added)
docs_result['new_source_comment_identifiers_absent'] = True
save('docs-and-whitespace-audit.json', docs_result)
sig = json.loads(subprocess.check_output(['gh', 'api', 'repos/kebag-logic/milan-fpga/commits/' + REF,
    '--jq', '{sha: .sha, verification: .commit.verification}']))
sig['git_signature_header_present'] = b'\ngpgsig ' in git('cat-file', 'commit', REF).split(b'\n\n')[0]
save('packet-signature.json', sig)
print('PASS: packet hashes, 80 identity pairs and older baseline, supersession links, unchanged executable ASTs')
print('Signature:', sig['verification']['reason'])
