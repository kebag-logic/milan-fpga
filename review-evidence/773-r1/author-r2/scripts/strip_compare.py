"""Show a SystemVerilog file is identical between two revisions once its comments are stripped.

usage: python3 -I strip_compare.py <repo> <rev-a> <rev-b> <path>
Strips /* ... */ blocks and // to end of line (no string literal in the file holds either), then compares the
remaining text byte for byte, and again with every whitespace run collapsed to one space.
"""
import hashlib, re, subprocess, sys

repo, a, b, path = sys.argv[1:5]


def strip(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return re.sub(r'//[^\n]*', '', text)


def show(rev):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], check=True, capture_output=True, text=True).stdout


ra, rb = show(a), show(b)
sa, sb = strip(ra), strip(rb)
na, nb = ' '.join(sa.split()), ' '.join(sb.split())
for name, x, y in (('raw', ra, rb), ('comments stripped', sa, sb), ('stripped, whitespace collapsed', na, nb)):
    ha, hb = (hashlib.sha256(v.encode()).hexdigest() for v in (x, y))
    print(f'{name}: {a} {ha[:16]} {b} {hb[:16]} {"IDENTICAL" if x == y else "DIFFERENT"}')
sys.exit(0 if na == nb else 1)
