#!/usr/bin/env python3
"""Check the bounded round-two delta without running broad build banks."""
import ast
import re
import subprocess
import sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
old = "75db4b57cff47bb614d14dead084649a4c2aa2a3"
head = "d4a27e6334118c9eef1023aa27e9fd2b7de9f076"
def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])
def read(rev, path):
    return git("show", f"{rev}:{path}").decode()
assert git("rev-parse", "HEAD").decode().strip() == head
paths = git("diff", "--name-only", old, head).decode().splitlines()
assert len(paths) == 5, paths
lex = re.compile(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/', re.S)
def no_comments(s):
    return lex.sub(lambda m: m[0] if m[0].startswith('"') else " ", s)
for path in [p for p in paths if p.endswith(".sv")]:
    a,b=(no_comments(read(r,path)) for r in (old,head))
    assert a.split() == b.split(), path
    print("PASS executable RTL unchanged:", path)
path="tb/verilator/avtp_rxmon/sim_main.cpp"
a,b=(no_comments(read(r,path)) for r in (old,head))
pat=r'printf\("\\n\[28\].*?\);'
assert len(re.findall(pat,a,re.S)) == len(re.findall(pat,b,re.S)) == 1
for s in (a,b):
    assert 'ck("[28d] 0ch rejected", dut->cnt_unsupported_fmt_o, 1)' in s
norm=lambda s: re.sub(pat,lambda m:'printf("BANNER");',s,flags=re.S).replace('(BAF family)','(family compare)')
assert norm(a).split() == norm(b).split()
print("PASS C++ stimuli/assertions unchanged; only [28] printf and [28e] label differ")
class Normalize(ast.NodeTransformer):
    def visit_FunctionDef(self,node):
        if node.name == "wire_truth": node.name = "instrument_channel_family"
        if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str): node.body=node.body[1:]
        return self.generic_visit(node)
    def visit_Attribute(self,node):
        if node.attr == "wire_truth": node.attr="instrument_channel_family"
        return self.generic_visit(node)
    def visit_Constant(self,node):
        if node.value == "wire-truth channel count (declared-vs-wire mismatch)":
            node.value="flat instrument family compare: any channel count accepted (the device listener rejects, #765)"
        if isinstance(node.value,str): node.value=node.value.replace("accepted (wire truth)","accepted (family compare)")
        return node
path="tb/verilator/tsn_fuzz/fuzz_aaf.py"
a,b=(ast.dump(Normalize().visit(ast.parse(read(r,path))),include_attributes=False) for r in (old,head))
assert a==b
print("PASS Python AST unchanged after explicit method/docstring/section/check-label normalization")
path="hdl/ieee1722/avtp/doc/TEST_RESULTS.md"
a,b=(read(r,path) for r in (old,head))
a=a.replace("wire-truth channel count (declared-vs-wire mismatch)","flat instrument family compare: any channel count accepted (the device listener rejects, #765)").replace("accepted (wire truth)","accepted (family compare)")
normalize_stamp=lambda s: re.sub(r"(?m)^(\*\*PASS\*\*.*) · +\d{4}-\d{2}-\d{2} \d{2}:\d{2}$",r"\1",s)
assert normalize_stamp(a)==normalize_stamp(b)
print("PASS generated record differs only by declared section, five labels and timestamp; 164/0 unchanged")
added=[s[1:] for s in git("diff","--unified=0",old,head).decode().splitlines() if s.startswith("+") and not s.startswith("+++")]
assert not any(re.search(r"\bR67[34]\b|issuecomment-|\bB\d{2}\b",s) for s in added)
print("PASS added text contains no review identity, issue-comment ID or numbered bench label")
subprocess.run(["git","-C",str(repo),"diff","--check",old,head],check=True)
print("PASS whitespace diff check")
