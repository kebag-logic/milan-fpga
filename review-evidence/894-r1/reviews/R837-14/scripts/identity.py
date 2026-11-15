#!/usr/bin/env python3
"""Identity probes for round 20: rows_grade.py docstring-only change, aecp_mbx.h comment-only change.
Usage: python3 -I identity.py <repo> <old-rev> <new-rev>"""
import ast, re, subprocess, sys
repo, old, new = sys.argv[1:4]
def show(rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True, text=True, check=True).stdout
def strip_doc(src):
    t = ast.parse(src)
    doc = ast.get_docstring(t, clean=False)
    t.body = t.body[1:]
    return doc, ast.dump(t, include_attributes=True)
rg = 'tb/verilator/ctrl_service_budget/rows_grade.py'
a, b = show(old, rg), show(new, rg)
(da, ta), (db, tb) = strip_doc(a), strip_doc(b)
print('rows_grade AST without docstring identical (positions):', ta == tb)
print('rows_grade line count', len(a.splitlines()), len(b.splitlines()))
pa = da.split('Sources, and their arrival bound')[1]; pb = db.split('Sources, and their arrival bound')[1]
print('documented() part identical:', pa == pb)
sa = set(re.findall(r'^  ([a-z]+) {2,}', pa, re.M)); sb = set(re.findall(r'^  ([a-z]+) {2,}', pb, re.M))
print('documented() sets', sorted(sa) == sorted(sb), len(sb), sorted(sb))
print('description first paragraph', repr(db.split('\n\n')[0][:60]))
hdr = 'sw/firmware/ctrl/aecp/aecp_mbx.h'
def toks(src):
    src = re.sub(r'/\*.*?\*/', ' ', src, flags=re.S)
    src = re.sub(r'//[^\n]*', '', src)
    return re.findall(r'[A-Za-z_]\w*|\d\w*|"(?:\\.|[^"\\])*"|\S', src)
ha, hb = show(old, hdr), show(new, hdr)
print('aecp_mbx.h tokens identical:', toks(ha) == toks(hb), 'lines', len(ha.splitlines()), len(hb.splitlines()))
# preprocessor-based check too
for rev, src in ((old, ha), (new, hb)):
    pass
