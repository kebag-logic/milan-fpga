"""Compare a C file's text with // and /* */ comments and blank runs removed, at two revisions.
Usage: python3 -I code_tokens.py <repo> <rev-a> <rev-b> <path>...  (prints SAME or the differing code lines)"""
import re, subprocess, sys
repo, a, b, *paths = sys.argv[1:]
def code(rev, p):
    t = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{p}'], capture_output=True, text=True, check=True).stdout
    t = re.sub(r'/\*.*?\*/', ' ', t, flags=re.S)
    t = re.sub(r'//[^\n]*', '', t)
    return [' '.join(l.split()) for l in t.split('\n') if l.strip()]
for p in paths:
    x, y = code(a, p), code(b, p)
    if x == y:
        print(f'SAME {p}')
    else:
        import difflib
        print(f'DIFF {p}'); print('\n'.join(l for l in difflib.unified_diff(x, y, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')))
