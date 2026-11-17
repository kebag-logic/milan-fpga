"""The source-comment rule's scan of a delta: every added line of a non-Markdown file in BASE..HEAD that shows an
issue-comment ID or review-round wording. Read only; exit 1 when any line is listed.
usage: python3 -I comment_scan.py CHECKOUT BASE [HEAD]   (no HEAD: the working tree)"""
import re
import subprocess
import sys

root, base = sys.argv[1], sys.argv[2]
head = sys.argv[3] if len(sys.argv) > 3 else None
#: an issue-comment ID; review-round wording: a numbered round or phase, a reviewer's or author's label, "re-review"
RULES = [('issue-comment ID', re.compile(r'issuecomment-?\d*')),
         ('a numbered round', re.compile(r'\b[Rr]ounds? \d|\b[Rr]ound-\d|\b[Rr]ound \(?[ivx]+\)')),
         ('a phase', re.compile(r'\b[Pp]hase [A-D]\b')),
         ('a review label', re.compile(r'\b[RA]\d{3,4}(-\d+)?\b|\bR\d{3}-\d')),
         ('review wording', re.compile(r'\b(re-?review|reviewer|REVIEW READY|TAKEN|STOP comment)\b'))]
diff = subprocess.run(['git', '-C', root, 'diff', '--unified=0', '--no-color', base, *([head] if head else [])], check=True,
                      capture_output=True, text=True).stdout
path, line, hits = '', 0, []
for s in diff.splitlines():
    if s.startswith('+++ '):
        path = s[6:] if s.startswith('+++ b/') else ''
    elif s.startswith('@@'):
        line = int(re.search(r'\+(\d+)', s)[1]) - 1
    elif s.startswith('+') and path:
        line += 1
        if path.endswith('.md'):
            continue
        for name, rule in RULES:
            if rule.search(s[1:]):
                hits.append(f'{path}:{line}: [{name}] {s[1:].strip()}')
                break
print(f'# {base[:12]}..{head or "the working tree"}: added non-Markdown lines with an issue-comment ID or review-round wording: {len(hits)}')
print('\n'.join(hits))
sys.exit(1 if hits else 0)
