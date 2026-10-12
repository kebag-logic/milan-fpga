"""Compare completed baseline and merge-head validation records."""
from pathlib import Path
from collections import Counter
import difflib
import hashlib
import json
import re
import sys
r=Path('$VALIDATION_STORAGE/pp73-a595/r5')
out=r/'comparisons';out.mkdir(exist_ok=True)
def zero(path):
    assert path.read_text().strip()=='0',str(path)
def save(name,lines):
    text='\n'.join(lines)+'\n';(out/(name+'.txt')).write_text(text);print(text,end='')
def static():
    lines=[]
    for name in ['check','lint','matrix','yosys','guard-portability']:
        for side in ['base','head']:zero(r/'logs'/f'{side}-{name}.rc')
        b,h=[(r/'logs'/f'{side}-{name}.log').read_text() for side in ['base','head']]
        if name=='check':
            comparable=[x for x in h.splitlines() if not x.startswith(('field drift:','aecp commands'))]
            comparable=[x.replace('links: 1192 checked','links: 1191 checked').replace('ids: 578 files','ids: 569 files').replace('226 tags in 19 files','225 tags in 18 files') for x in comparable]
            assert Counter(comparable)==Counter(b.splitlines()),name
            assert len([x for x in h.splitlines() if x.startswith('field drift:')])==30
            details='every existing result identical; only added command checks, 1 link, 9 source files and 1 execution tag in 1 file differ; completion order ignored'
        else:
            assert b==h,name
            details='raw logs byte-identical'
        lines.append(f'{name}: base/head rc 0; {details}')
        (out/(name+'.diff')).write_text(''.join(difflib.unified_diff(b.splitlines(True),h.splitlines(True),fromfile='base',tofile='head')))
    save('static',lines)
def suites():
    for side in ['base','head']:zero(r/'logs'/f'{side}-suites.rc')
    b,h=[(r/'logs'/f'{side}-suites.log').read_text().splitlines() for side in ['base','head']]
    bc=[x for x in b if not x.startswith('suites:')]
    hc=[x for x in h if not x.startswith(('suites:','PASS aecp_cmds '))]
    assert bc==hc,'common suite records differ'
    added=[x for x in h if x.startswith('PASS aecp_cmds ')]
    assert added==['PASS aecp_cmds (176 checks: 176 PASS, 0 FAIL)'],added
    save('suites',['base/head rc 0; every common suite record byte-identical',b[-1],h[-1],*added])
def parent():
    lines=[]
    for side in ['base','head']:
        bank=r/'parent-e8454e27'/side
        codes=list(bank.glob('*.rc'));assert len(codes)==5
        for path in codes:zero(path)
        lines.append(f'{side}: all five scratch-parent commands rc 0')
    for name in ['bdd','feature_status','pp_srcs','rom_verify_tcam']:
        b,h=[(r/'parent-e8454e27'/side/(name+'.log')).read_text() for side in ['base','head']]
        def norm(s):return re.sub(r'Took .*','Took <elapsed>',re.sub(r'\d+\.\d+s','<seconds>',s))
        assert norm(b)==norm(h),name
        lines.append(f'{name}: raw byte-identical {b==h}; records identical ignoring elapsed durations only')
    rows=[]
    for side in ['base','head']:
        rows.append(['\t'.join(x.split('\t')[1:]) for x in (r/'parent-e8454e27'/side/'rom_rows_at_pin.tsv').read_text().splitlines()])
    assert rows[0]==rows[1]
    lines.append('ROM ledger rows identical apart from commit key')
    for name in ['check','list','selftest']:zero(r/'logs'/f'head-python-{name}.rc')
    old=(r.parent/'r4/logs/head-python.log').read_text().splitlines()[1:]
    new=(r/'logs/head-python-check.log').read_text().splitlines()[1:]
    assert new==old,'source-style counts or budgets changed'
    lines.append('Consumer source-style check/list/54-check self-test rc 0; all counts and budgets unchanged from round 4')
    save('parent',lines)
for arg in sys.argv[1:] or ['static','parent']:
    globals()[arg]()
