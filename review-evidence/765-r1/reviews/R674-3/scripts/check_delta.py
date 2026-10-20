#!/usr/bin/env python3
"""Bounded equivalence checks for the assigned round-three delta."""
import ast,re,subprocess,sys
from pathlib import Path
repo=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
HEAD='87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d'
BASE='d4a27e6334118c9eef1023aa27e9fd2b7de9f076'
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args],text=True)
def old(path): return git('show',BASE+':'+path)
def new(path): return (repo/path).read_text()
assert git('rev-parse','HEAD').strip()==HEAD
paths=git('diff','--name-only',BASE,HEAD).splitlines()
assert set(paths)=={'hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv','hdl/ieee1722/avtp/doc/TEST_RESULTS.md','tb/verilator/avtp_rxmon/sim_main.cpp','tb/verilator/tsn_fuzz/fuzz_aaf.py'}
print('Exact four-path delta; one child commit:',git('rev-list','--count',BASE+'..'+HEAD).strip())
# Compare comment-stripped tokens; the changed region is entirely a comment.
def tokens(s):
    s=re.sub(r'//[^\n]*|/\*.*?\*/','',s,flags=re.S)
    return re.findall(r'[A-Za-z_$][A-Za-z0-9_$]*|[0-9]+|[^\s]',s)
sv=paths[0]
assert sv.endswith('.sv')
assert tokens(old(sv))==tokens(new(sv))
print('Flat SV: identical comment-stripped tokens')
cpp='tb/verilator/avtp_rxmon/sim_main.cpp'
def omit_banner(s):
    start=s.index('        printf(',s.index('void channel_freedom_accepts_every_count()'))
    end=s.index(');',start)+2
    return s[:start]+'BANNER'+s[end:]
assert omit_banner(old(cpp))==omit_banner(new(cpp))
print('Flat C++: byte-identical outside the [28] printf banner')
py='tb/verilator/tsn_fuzz/fuzz_aaf.py'
a,b=ast.parse(old(py)),ast.parse(new(py))
def normalize(tree,is_new):
    method=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='instrument_channel_family')
    method.body=method.body[1:] # the independently inspected docstring
    if is_new:
        assign=method.body.pop(0)
        assert isinstance(assign,ast.Assign) and ast.literal_eval(assign.value)==(1,2,3,4,8)
        loop=next(n for n in method.body if isinstance(n,ast.For))
        assert isinstance(loop.iter,ast.Name) and loop.iter.id=='counts'
        loop.iter=assign.value
    section=method.body[0]
    assert isinstance(section,ast.Expr) and isinstance(section.value,ast.Call) and section.value.func.attr=='section'
    method.body.pop(0) # section title only; full body and remaining module compared
    return ast.dump(tree,include_attributes=False)
assert normalize(a,False)==normalize(b,True)
print('Python: identical AST after checked tuple substitution, docstring/title removal')
md='hdl/ieee1722/avtp/doc/TEST_RESULTS.md'
oldtitle='flat instrument family compare: any channel count accepted (the device listener rejects, #765)'
newtitle="flat instrument family compare: channels_per_frame 1, 2, 3, 4, 8 accepted (the device listener rejects a count other than its current format's, #765)"
assert old(md).count(oldtitle)==2 and new(md).count(newtitle)==2
def stamp(s): return re.sub(r'2026-10-20 \d\d:\d\d','STAMP',s)
assert stamp(old(md).replace(oldtitle,newtitle))==stamp(new(md))
print('Generated artifact: only two section titles and generation timestamp changed')
assert 'channels_per_frame[7:0]' in new(sv)
assert 'a count of 256 is rejected' in new(sv)
assert 'channels_per_frame[7:0]' in new(cpp)
assert 'channels_per_frame[7:0]' in new(py)
for path in ['hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv','hdl/ieee1722/crf/KL_crf_rx.sv','tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv','tb/verilator/avtp_rxmon/sim_main_nx.cpp','tb/verilator/avtp_rxmon/format_mutants.py','tb/verilator/crf_rx/mutants.py','hdl/milan/milan_datapath.sv']:
    assert old(path)==new(path),path
print('Production context/CRF/datapath and prior finding/test artifacts unchanged')
subprocess.run(['git','-C',str(repo),'diff','--check',BASE,HEAD],check=True)
print('PASS: delta equivalence and whitespace')
