#!/usr/bin/env python3
"""Compare public approval text to the reviewed source; never change either."""
import argparse
import html
from pathlib import Path
import re
import subprocess

BASE = '423ac5d910d09ab189b3acc39ae3ae1d10d50b19'
PREVIOUS = 'a27808375427859dc357f6bfd0a88842062b20ed'

def prose(s):
    # PR tables encode pipes/newlines; repository-relative links become labels.
    return re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', html.unescape(s.replace('<br>', '\n')))

def section(s, start, end):
    return s.split(start, 1)[1].split(end, 1)[0].strip()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo', type=Path)
    ap.add_argument('pr_body', type=Path)
    a = ap.parse_args()
    pr = a.pr_body.read_text()
    sources = {name: (a.repo / name).read_text() for name in
               ['REQUIREMENTS.md', 'docs/reference/FR_NFR.md',
                'docs/traceability/ieee8021q.md', 'docs/design/MAILBOX_SPLIT.md']}
    def at(rev, path):
        return subprocess.check_output(['git', '-C', str(a.repo), 'show', rev + ':' + path], text=True)
    reviewed = False
    count = 0
    for line in pr.splitlines():
        if line.startswith('### Round-2 changes'):
            reviewed = True
        if not line.startswith('|'):
            continue
        cells = [prose(x.strip()) for x in line.strip('|').split('|')]
        if len(cells) != 3:
            continue
        label, old, new = cells
        if '&#124;' not in line and label not in ['REQUIREMENTS.md Section 1', 'MAILBOX_SPLIT listener discovery']:
            continue
        path = 'docs/reference/FR_NFR.md'
        if label == 'IEEE 802.1Q: MRP-6':
            path = 'docs/traceability/ieee8021q.md'
        if label == 'REQUIREMENTS.md Section 1':
            path = 'REQUIREMENTS.md'
            current = prose(section(sources[path], '## 1. Product ownership', '## 2. Reference standards'))
            previous = prose(section(at(BASE, path), '## 1. Product ownership', '## 2. Reference standards'))
            assert new == current and old == previous, label
        elif label == 'MAILBOX_SPLIT listener discovery':
            path = 'docs/design/MAILBOX_SPLIT.md'
            assert new in prose(sources[path]), label
            assert old in prose(at(PREVIOUS, path)), label
        else:
            assert '| ' + new + ' |' in prose(sources[path]), label + ': candidate differs'
            previous = prose(at(PREVIOUS if reviewed else BASE, path))
            if old.startswith('Absent:'):
                assert '| ' + label + ' |' not in previous, label + ': old row exists'
            else:
                assert '| ' + old + ' |' in previous, label + ': old text differs'
        count += 1
        print('PASS exact old/new approval text: ' + label)
    start = '### 3.4.1 Control service budget and normative timing'
    current = start + section(sources['docs/reference/FR_NFR.md'], start, '### 3.5 Resource, reliability, and the rest')
    approved = start + section(pr, start, 'The corresponding changed architecture')
    assert prose(current) == prose(approved), 'complete timing/hook block differs'
    print('PASS complete timing/hook block, including prose and every timing/transition row')
    assert count == 27, ('approval row population', count)
    for label in ['MAAP PROBE and conflict DEFEND', 'MAAP ANNOUNCE and reallocation']:
        line = next(x for x in sources['docs/reference/FR_NFR.md'].splitlines() if x.startswith('| ' + label + ' |'))
        assert line in pr, label + ': primary approval table differs at byte level'
        print('PASS byte-identical primary approval row: ' + label)
    assert 'Relates to #664' in pr and 'Closes #664' not in pr
    assert not re.search(r'unpublished|not pushed|do not push', pr, re.I)
    print('PASS publication wording and approval-pending linkage')
    print('PASS: 27 old/new entries and complete timing/hook text; only presentation links/HTML encoding normalized')

if __name__ == '__main__':
    main()
