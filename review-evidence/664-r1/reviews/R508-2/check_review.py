#!/usr/bin/env python3
"""Read-only exact-head and public approval-text checks. No network writes."""
import argparse
import hashlib
import html
import os
from pathlib import Path
import re
import stat
import subprocess

HEAD = '8fb296e3e02985aee27ef04cb08278836b734a14'
TREE = 'ce846f8ab472d3c9bf605598224ae2521966d928'
BASE = '423ac5d910d09ab189b3acc39ae3ae1d10d50b19'
PREVIOUS = 'a27808375427859dc357f6bfd0a88842062b20ed'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args],
                                   env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})


def identity(repo, revision, label):
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == revision
    expected = {}
    entries = git(repo, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0')
    count = 0
    for entry in filter(None, entries):
        meta, name = entry.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid)
        if kind == b'commit':
            continue
        path = repo / os.fsdecode(name)
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, name
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert actual == oid, name
        count += 1
    indexed = {}
    for entry in filter(None, git(repo, 'ls-files', '--stage', '-z').split(b'\0')):
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and name not in indexed, name
        indexed[name] = (mode, oid)
    assert indexed == expected, 'index differs from commit'
    print(f'PASS {label}: {revision}; {count} raw blobs/symlinks, modes, complete index')
    return expected


def rendered(text):
    text = re.sub(r'\[([^\]]+)\]\([^\n)]+\)', r'\1', text)
    return html.unescape(text.replace('<br>', '\n'))


def section(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', type=Path)
    ap.add_argument('pr_body', type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    assert git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    entries = identity(repo, HEAD, 'parent')
    for name in ['third_party/verilog-axis', 'protocol-processor', 'gptp-processor']:
        mode, pin = entries[name.encode()]
        assert mode == b'160000'
        assert (repo/name/'.git').is_file(), 'registered submodule required'
        identity(repo/name, pin.decode(), name)
    changed = git(repo, 'diff', '--name-only', BASE, HEAD).decode().splitlines()
    assert len(changed) == 21 and all(p.endswith('.md') for p in changed)
    r2 = git(repo, 'diff', '--name-only', PREVIOUS, HEAD).decode().splitlines()
    assert r2 == ['docs/design/MAILBOX_SPLIT.md', 'docs/reference/FR_NFR.md']
    print('PASS scope: 21 Markdown files; round 2 exactly two documentation files')
    pr = args.pr_body.read_text()
    fr = (repo/'docs/reference/FR_NFR.md').read_text()
    requirement_row = next(line for line in pr.splitlines()
                           if line.startswith('| REQUIREMENTS.md Section 1 |'))
    cells = [cell.strip() for cell in requirement_row.strip('|').split('|')]
    for revision, quoted in [(BASE, cells[1]), (HEAD, cells[2])]:
        requirements = git(repo, 'show', revision+':REQUIREMENTS.md').decode()
        text = section(requirements, '## 1. Product ownership', '## 2. Reference standards')
        assert rendered(text) == rendered(quoted), 'REQUIREMENTS section 1'
    print('PASS approval: REQUIREMENTS section 1 old/new visible text matches exactly')
    for title, end in [('### 3.4.1 Control service budget and normative timing',
                        '### 3.4.2 Control service test hooks'),
                       ('### 3.4.2 Control service test hooks',
                        '### 3.5 Resource, reliability, and the rest')]:
        actual = section(fr, title, end)
        pr_end = end if title.startswith('### 3.4.1') else 'The corresponding changed architecture and traceability rows follow.'
        approved = section(pr, title, pr_end)
        assert rendered(actual) == approved, title
        print('PASS approval exact text, links reduced to their visible label:', title)
    base_fr = git(repo, 'show', BASE+':docs/reference/FR_NFR.md').decode()
    rows = 0
    for line in pr.splitlines():
        if not re.match(r'\| (FR-|NFR-)', line):
            continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        if len(cells) != 3:
            continue
        key, old, new = cells
        for contents, quoted in [(base_fr,old),(fr,new)]:
            source = next(x for x in contents.splitlines() if x.startswith('| '+key+' |'))
            assert source.strip('|').strip() == html.unescape(quoted), key
        rows += 1
    assert rows == 8
    print('PASS approval: all eight changed FR/NFR old/new rows match exactly')
    block = section(pr, '### Round-2 changes from the reviewed candidate',
                    'H-DISC shares one T_svc')
    old_fr = git(repo, 'show', PREVIOUS+':docs/reference/FR_NFR.md').decode()
    mailbox = (repo/'docs/design/MAILBOX_SPLIT.md').read_text()
    old_mailbox = git(repo, 'show', PREVIOUS+':docs/design/MAILBOX_SPLIT.md').decode()
    r2_rows = 0
    for line in block.splitlines():
        if not line.startswith('| ') or line.startswith('| Row |'):
            continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        if len(cells) != 3:
            continue
        key, old, new = cells
        if key == 'MAILBOX_SPLIT listener discovery':
            begin = "The listener's discovery machine (5.6.4)"
            for contents, quoted in [(old_mailbox,old),(mailbox,new)]:
                source = begin + section(contents, begin, '### Service latency')
                # section strips the leading space before 'feeds'.
                source = source.replace('(5.6.4)feeds', '(5.6.4) feeds')
                assert rendered(source) == rendered(quoted), key
        else:
            for contents, quoted in [(old_fr,old),(fr,new)]:
                matches = [x for x in contents.splitlines() if x.startswith('| '+key+' |')]
                if quoted.startswith('Absent:'):
                    assert not matches, key
                else:
                    assert len(matches) == 1, key
                    assert matches[0].strip('|').strip() == html.unescape(quoted), key
        r2_rows += 1
    assert r2_rows == 11
    print('PASS approval: all 11 round-2 old/new rows match head and prior head')
    assert 'not pushed' not in pr and 'unpublished branch' not in pr.lower()
    assert 'PR #674 already exists' in pr and HEAD in pr
    print('PASS PR publication wording and head identity')
    print('PASS all checks; no tracked files written')


if __name__ == '__main__':
    main()
