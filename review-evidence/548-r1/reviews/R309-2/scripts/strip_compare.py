#!/usr/bin/env python3
"""Compare comment-stripped HDL between two commits for every tracked HDL path.
Usage: strip_compare.py <repo> <base> <head>. Exit 0 iff all identical and a
nonzero-tie control mutation is detected."""
import re, subprocess, sys
repo, base, head = sys.argv[1:4]
EXT = ('.sv', '.svh', '.v', '.vh')
def git(*a):
    return subprocess.run(['git', '-C', repo, *a], check=True, capture_output=True).stdout
def files(rev):
    return {p for p in git('ls-tree', '-r', '--name-only', rev).decode().splitlines() if p.endswith(EXT)}
def strip(src):
    out, i, n, s = [], 0, len(src), None
    while i < n:
        c = src[i]
        if s:
            out.append(c)
            if c == '\\': out.append(src[i+1:i+2]); i += 2; continue
            if c == '"': s = None
            i += 1; continue
        if c == '"': s = c; out.append(c); i += 1; continue
        if src.startswith('//', i):
            j = src.find('\n', i); i = n if j < 0 else j; continue
        if src.startswith('/*', i):
            j = src.find('*/', i + 2); i = n if j < 0 else j + 2; out.append(' '); continue
        out.append(c); i += 1
    toks = re.sub(r'\s+', ' ', ''.join(out)).strip()
    return toks
fb, fh = files(base), files(head)
bad = 0
if fb != fh:
    print('FILESET DIFFERS', sorted(fb ^ fh)); bad = 1
for p in sorted(fb & fh):
    a = strip(git('show', f'{base}:{p}').decode('utf-8', 'replace'))
    b = strip(git('show', f'{head}:{p}').decode('utf-8', 'replace'))
    if a != b:
        print('DIFF', p); bad = 1
print(f'compared {len(fb & fh)} HDL files base={base} head={head}: {"IDENTICAL" if not bad else "DIFFERENT"}')
# control: a nonzero tie must be detected
p = 'hdl/milan/milan_datapath.sv'
h = git('show', f'{head}:{p}').decode()
m = h.replace("assign aecp_ctlr_diag = 32'd0;", "assign aecp_ctlr_diag = 32'h01001001;")
assert m != h, 'control anchor missing'
ctl = strip(m) != strip(h)
print('control nonzero-tie mutation detected:', ctl)
sys.exit(0 if (not bad and ctl) else 1)
