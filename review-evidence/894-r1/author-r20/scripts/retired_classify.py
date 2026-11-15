#!/usr/bin/env python3
"""Class every line retired_artifacts.py lists (argv[1]); argv[2] is the PR body it read. Exits 1 on any it does not
class."""
import re
import sys

S, F = 'docs/design/SPLIT_CONTROL_MEMORY.md', 'docs/reference/FR_NFR.md'
RG = 'tb/verilator/ctrl_service_budget/rows_grade.py'
C = {
    f'{S}:2194': ('historical', "'the loop search's, before THE TIERS retired it ... was ... held'"),
    f'{S}:2200': ('historical', "'Before the tiers, a search of the loop's choices (ctrl_retry_search.py) held ... the search is retired'"),
    f'{S}:2244': ('historical', "'which the loop search (ctrl_retry_search.py, retired by #894) held the loop to'"),
    f'{F}:390': ('historical', "'the loop search's, before THE TIERS retired it ... held ... failed it then'"),
    'sw/firmware/ctrl/aecp/aecp_mbx.h:23': ('historical', "'the retry search, before THE TIERS retired it, held'"),
    f'{RG}:5': ('historical', "rows_grade.py's docstring: 'rows_tiers.py's rows under THE TIERS (the loop search's before)' (41ca9f87)"),
    f'{RG}:19': ('historical', "rows_grade.py's docstring: 'which the loop search held the loop to' (41ca9f87)"),
    f'{RG}:20': ('historical', "rows_grade.py's docstring: 'once derived from the loop's constants and held' (41ca9f87)"),
    f'{RG}:21': ('historical', "rows_grade.py's docstring: 'by the loop search, now queued_bound.py's rule' (41ca9f87)"),
}


def main(path, body):
    sec, cur = [], ''
    for s in open(body, encoding='utf-8').read().split('\n'):
        if re.match(r'#{2,3} ', s):
            cur = s.strip()
        sec.append(cur)
    rows, bad, head, counts = [], 0, '', {}
    for line in open(path, encoding='utf-8'):
        if line.startswith('#'):
            head = line.strip()
            continue
        f, n, art, text = line.rstrip('\n').split('\t', 3)
        c = C.get(f'{f}:{n}')
        if c is None and f == 'PR-BODY' and sec[int(n) - 1].startswith(('## Round 2', '### 20.', '## Findings', '## Known')):
            c = ('historical', f"this body's round-20 text, finding row or limitation ({sec[int(n) - 1][:30]})")
        if c is None:
            bad += 1
            rows.append(f'UNCLASSIFIED\t{f}:{n}\t{text[:140]}')
            continue
        counts[c[0]] = counts.get(c[0], 0) + 1
        rows.append(f'{c[0]}\t{f}:{n}\t{c[1]}')
    print("# Round 20, R837-13-S1: every line naming a file this PR deletes, by path, name, stem or prose name, each classed")
    print(head)
    print('# ' + ', '.join(f'{k} {v}' for k, v in sorted(counts.items())) + f', total {len(rows)}, unclassified {bad}; current: 0')
    for r in rows:
        print(r)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
