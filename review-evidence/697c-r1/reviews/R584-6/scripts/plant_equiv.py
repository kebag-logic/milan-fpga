#!/usr/bin/env python3
"""For every control-firmware mutant, plant it into its file at a base checkout (its own cores) and at a
head checkout (cores from third_party/tsn-c-stack), each with that checkout's own table, and compare the
planted files token for token (comments and whitespace ignored). Unplanted files are compared too.
Usage: python3 -B plant_equiv.py <base-checkout> <head-checkout>"""
import re, subprocess, sys, json
from pathlib import Path
TOK = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|[A-Za-z_]\w*|\d[\w.]*|\S', re.S)
def toks(s): return [t for t in TOK.findall(s) if not t.startswith(('//', '/*'))]
def table(root):
    code = ("import sys,json;sys.path[:0]=[%r,%r];import ctrl_mutants as c;"
            "print(json.dumps([[m.name,m.path,m.old,m.new] for m in c.MUTANTS]))") % (
        str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest'))
    return {r[0]: r[1:] for r in json.loads(subprocess.run([sys.executable, '-B', '-c', code], cwd=root,
                                                           capture_output=True, text=True, check=True).stdout)}
def resolve(root, path):
    return root / 'third_party/tsn-c-stack' / path.removeprefix('tsn-c-stack/') if path.startswith('tsn-c-stack/') \
        else root / 'sw/firmware/ctrl' / path
base, head = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
tb, th = table(base), table(head)
same = differ = bad = 0
for name in sorted(tb):
    pb, ob, nb = tb[name]; ph, oh, nh = th[name]
    xb, xh = resolve(base, pb).read_text(), resolve(head, ph).read_text()
    if xb.count(ob) != 1 or xh.count(oh) != 1:
        print(f"ANCHOR {name}: base {xb.count(ob)} head {xh.count(oh)}"); bad += 1; continue
    if toks(xb.replace(ob, nb)) == toks(xh.replace(oh, nh)):
        same += 1
    else:
        differ += 1; print(f"DIFFER {name} {pb} {ph}")
print(f"planted programs token-identical: {same}; differing: {differ}; anchor faults: {bad}; total {len(tb)}")
sys.exit(1 if differ or bad else 0)
