#!/usr/bin/env python3
"""Verify the two public corrections against the immutable source objects."""
import argparse
import copy
import json
import re
import subprocess
from pathlib import Path

BASE = '6714181d0c8a16e2983f85b724f4d688f5111835'
HEAD = '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'
README = 'sw/firmware/gtest/README.md'


def rows(doc):
    table = doc.split('| File | Function | Statement | Uncovered | Why no input reaches it |\n', 1)[1]
    result = []
    for line in table.splitlines()[1:]:
        if not line.startswith('|'):
            break
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        assert len(cells) == 5, 'unexpected table structure'
        result.append(cells)
    return result


def citation_ok(body):
    bullet = next(line for line in body.splitlines() if line.startswith('- `sw/firmware/ctrl/adp/adp.h`:'))
    return bool(re.search(r'Milan v1\.2 section 5\.6\.3 \(Advertise state machine\)', bullet)
                and re.search(r'IEEE 1722\.1-2021 section 6\.2 \(ADPDU\)', bullet))


def correction_ok(body):
    return ('14 data rows, unchanged from the source base; five are ADP rows.' in body
            and '6024328677' in body)


def exclusions_equal(before, after):
    return [row[:4] for row in before] == [row[:4] for row in after]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repository', type=Path)
    ap.add_argument('receipts', type=Path)
    args = ap.parse_args()
    def git(*cmd):
        return subprocess.check_output(['git', '--no-replace-objects', '-C', str(args.repository), *cmd], text=True)
    def artifact(name):
        return json.loads((args.receipts / name).read_text())
    before = rows(git('show', f'{BASE}:{README}'))
    after = rows(git('show', f'{HEAD}:{README}'))
    pr = artifact('pr-684.json')
    correction = artifact('comment-6024757146.json')
    original = artifact('comment-6024328677.json')
    assert pr['head']['sha'] == HEAD
    assert git('rev-parse', 'HEAD').strip() == HEAD
    assert citation_ok(pr['body'])
    assert correction_ok(correction['body'])
    assert len(before) == len(after) == 14
    assert sum(row[0] == '`sw/firmware/ctrl/adp/adp.c`' for row in before) == 5
    assert sum(row[0] == '`sw/firmware/ctrl/adp/adp.c`' for row in after) == 5
    assert exclusions_equal(before, after)
    assert 'Exclusion table unchanged (15 rows)' in original['body']
    assert original['created_at'] == original['updated_at']
    changed = git('diff', '--name-only', BASE, HEAD).splitlines()
    assert len(changed) == 26 and all(path.startswith('sw/firmware/') for path in changed)
    # Negative controls operate only on memory, never on the candidate checkout.
    assert not citation_ok(pr['body'].replace('Milan v1.2 section 5.6.3', 'Milan v1.2 section 5.3.1'))
    assert not correction_ok(correction['body'].replace('14 data rows', '15 data rows'))
    widened = copy.deepcopy(after)
    widened[0][3] = 'arcs 1, 2 of 2'
    assert not exclusions_equal(before, widened)
    for label, value in [('head', HEAD), ('base', BASE), ('PR updated', pr['updated_at']),
                         ('correction URL', correction['html_url']), ('original URL', original['html_url'])]:
        print(f'{label}: {value}')
    print('PASS F1: Advertise state machine = Milan v1.2 5.6.3; ADPDU = IEEE 1722.1-2021 6.2')
    print('PASS F2: base 14 rows / 5 ADP; head 14 rows / 5 ADP; all exclusion coordinates unchanged')
    print('PASS: original 15-row comment retained; created_at equals updated_at')
    print('PASS: 26 changed paths, all firmware; no RTL/configuration/workflow/gitlink delta')
    print('PASS: wrong-clause, wrong-count and widened-exclusion negative controls rejected (3/3)')
    for i, row in enumerate(after, 1):
        print(f'exclusion {i:02}: ' + ' | '.join(row[:4]))


if __name__ == '__main__':
    main()
