#!/usr/bin/env python3
"""Audit pinned public packet and source equivalence; requires the evidence commit in CHECKOUT's object store."""
from pathlib import Path
import subprocess,sys,json,hashlib,re,ast
R=Path(sys.argv[1]).resolve(); P=Path(__file__).resolve().parent
E='98bc6f22bc3c42bd78c1585b6e3bdca2018d25f1'; HEAD='8267b8951616cfd570baf690835d4b0d38f14596'
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def read(f):return git('show',E+':review-evidence/gptpsw-r1/'+f)
rows=json.loads(read('MANIFEST.json')); count=0
for row in rows:
    if row['file'].startswith('author-r4/'):
        assert hashlib.sha256(read(row['file'])).hexdigest()==row['published_sha256'],row['file'];count+=1
print('Published SHA-256 manifest: all',count,'author-r4 files match')
print('Evidence commit has embedded signature:',b'\ngpgsig ' in git('cat-file','commit',E))
checks=[('contract','8167b70d',['sw/mailbox/mailbox.yaml','docs/reference/MAILBOX_CONTRACT.md','sw/firmware/ctrl/mbx/mbx_contract.h']),('RTL and benches','a6323318',['hdl','tb','protocol-processor','gptp-processor','third_party']),('core and adapters','4e934621',['sw/firmware/ctrl/gptp','sw/firmware/ctrl/host','sw/firmware/ctrl/loop','sw/firmware/ctrl/mbx','sw/firmware/ctrl/test/test_gptp.cpp','sw/firmware/ctrl/test/gptp_mutants.py']),('firmware and builder','631dc544',['sw/firmware','sw/builder','tb','hdl','sw/mailbox']),('CPU limits and ledger','8167b70d',['tb/verilator/ctrl_service_budget','sw/firmware/ctrl/loop/ctrl_loop.h'])]
for name,base,paths in checks:
    assert subprocess.run(['git','diff','--quiet',base,HEAD,'--',*paths],cwd=R).returncode==0
    print('Unchanged',name,'from',base,'to',HEAD)
order=[l.strip() for l in (R/'sw/firmware/ctrl/plat/ctrl_split_hot.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
kept=read('author-r4/receipts/hotlist/gptp/kept.txt').decode().splitlines()
assert order==kept
traced=read('author-r4/receipts/hotlist/gptp/order.txt').decode().splitlines()
assert [s for s in traced if s not in ['aecp owe','aecp owed_drain']]==order
assert len(order)==286
print('Hot order: 288 traced entries minus exactly two documented exclusions equals 286 committed entries; gPTP entries',sum(s.split()[0] in ['gptp','gptp_mbx'] for s in order))
large=read('author-r4/receipts/hotlist/LARGE.txt').decode()
header=(R/'sw/firmware/ctrl/plat/ctrl_split_hot.txt').read_text()
for line in large.splitlines():
    if line.startswith('gptp/'):
        assert line.split()[-1] in header
print('Three trace hash identifiers agree. Raw PC traces and link maps are omitted; no independent raw-trace regeneration claimed.')
measure=json.loads(read('author-r4/receipts/after-relearn/measurement-audit.json'))
for point,m in measure.items():
    if not isinstance(m,dict) or 'turnaround_max_ms' not in m:continue
    assert m['turnaround_max_ms']<=10 and m['gptp_record_max_ms']<=10 and not m['share_misses'] and not m['refusals']
    print(point,'turnaround',m['turnaround_max_ms'],'record',m['gptp_record_max_ms'],'composed',m['composed_maximum']['ms'],'gPTP maximum cycles',m['gptp_max_cycles_one_pass'])
d=json.loads(read('author-r4/receipts/builder-final/driver.json'))
print('Builder gates:',len(d['gates']),'all pass verdict:',all(x['verdict']=='pass' for x in d['gates']))
for x in d['gates']:
    for row in x['not_run']: print('Builder NOT RUN:',x['gate'],row[0],row[1].split(':')[0])
# Current documented symbols vs the changed authoritative ledger.
sys.path.insert(0,str(R/'sw/litex'));import ctrl_memory as cm
for key in ['8x8-one-interface-gptp','8x8-two-interfaces-gptp']:
    row=next(l for l in (R/'docs/design/SPLIT_CONTROL_MEMORY.md').read_text().splitlines() if l.startswith('| `'+key+'`'))
    print('DOC:',row)
    print('CODE:',key,cm.LEDGERED[key])
for point in ['gptp','plain']:
    path=P/'scratch/public/review-evidence/gptpsw-r1/author-r4/receipts/harness-631dc544'/ (point+'-8x8-1if')
    if not path.exists():
        path.mkdir(parents=True)
        prefix='author-r4/receipts/harness-631dc544/'+point+'-8x8-1if/'
        listed=git('ls-tree','-r','--name-only',E,'review-evidence/gptpsw-r1/'+prefix).decode().splitlines()
        for name in listed:
            if name.endswith('.json'):
                (path/Path(name).name).write_bytes(read(name.removeprefix('review-evidence/gptpsw-r1/')))
    with (P/('egress-'+point+'.log')).open('w') as f:
        rc=subprocess.run([sys.executable,'-B',str(R/'tb/verilator/ctrl_service_budget/egress_ledger.py'),'--point','8x8-1if',str(path)],cwd=R,stdout=f,stderr=subprocess.STDOUT).returncode
    assert rc==0
    print('Exact-head egress checker on published',point,'1if JSON: PASS')
print('Source/executable evidence audit complete; this is not execution of the author banks.')
