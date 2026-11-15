#!/usr/bin/env python3
"""Class every line removed_constants.py lists (argv[1]); argv[2] is the PR body it read. Exits 1 on a line it does not
class. A section-13 line is classed by its own line, read; a PR-body line by the section it sits in (round 19's text
and its finding rows quote the old framing as history)."""
import re
import sys

S = 'docs/design/SPLIT_CONTROL_MEMORY.md'
C = {
    f'{S}:1970': ('historical', "the 2026-11-05 record: 'no longer held when this note was written'; THE TIERS since replaced the bounds; 'CTRL_LOOP_SRP_MS is removed'"),
    f'{S}:2010': ('historical', "'CTRL_LOOP_SRP_MS stated SRP's bound ... 18 ms ... Under THE TIERS it is removed', SRP's R5 and R6 rows beside it"),
    f'{S}:2519': ('historical', "'THE TIERS replace the three bounds the loop held by construction before them'"),
    f'{S}:2522': ('historical', "'CTRL_LOOP_SRP_MS (removed under THE TIERS), was THE SHARE's nine passes'"),
}


def main(path, body):
    sec, cur = [], ''
    for s in open(body, encoding='utf-8').read().split('\n'):
        if re.match(r'#{2,3} ', s):
            cur = s.strip()
        sec.append(cur)
    rows, bad, gone = [], 0, ''
    for line in open(path, encoding='utf-8'):
        if line.startswith('# gone:'):
            gone = line.strip()
            continue
        f, n, name, text = line.rstrip('\n').split('\t', 3)
        c = C.get(f'{f}:{n}')
        if c is None and f == 'PR-BODY' and sec[int(n) - 1].startswith(('## Round 19', '### 19.', '## Findings')):
            c = ('historical', f"this body's round-19 text or finding row ({sec[int(n) - 1][:30]}), quoting the old framing")
        if c is None:
            bad += 1
            rows.append(f'UNCLASSIFIED\t{f}:{n}\t{name}\t{text[:140]}')
            continue
        rows.append(f'{c[0]}\t{f}:{n}\t{name}\t{c[1]}')
    print("# Round 19, sweep 2: every line naming a #define of sw/firmware/ctrl at 66f71326 that the head defines nowhere in")
    print("# sw/ (removed_constants.py, the R837-12 reviewer's), each classed")
    print(gone)
    print(f"# {len(rows)} lines, unclassified {bad}; current: 0")
    for r in rows:
        print(r)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
