"""Copy the gate pass's receipts into the output directory: each root's tables, jobs.txt, driver logs, step logs and rc files.

usage: collect_gates.py <gates scratch> <receipts/gates>
A file over 200 KB is not copied; its sha256 and size go in large.sha256 beside where it would have been.
Clones, build trees and caches are never walked: only the roots' logs/, first-attempt*/ and cut-at-reset/ directories.
"""
import hashlib, shutil, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
LIMIT = 200 * 1024
TOP = ['rtl-fast-table.md', 'docs-yml-table.md', 'elaborate-table.md', 'rtl-table.md', 'HEAD',
       'not_run_rtl-fast.json', 'not_run_docs.json', 'not_run_elaborate.json', 'not_run_rtl.json',
       'run_wf.py', 'verify_wf.py', 'run_docs_yml.py', 'verify_docs_yml.py', 'run_step.py', 'wf_jobs.sh', 'docs_jobs.sh',
       'rtl.sh', 'extra.sh', 'extra2.sh', 'chainA.sh', 'chainB.sh', 'chainC.sh', 'chainD.sh', 'rerun_gptp.sh',
       'rerun_elab1.sh', 'extra-table.md', 'not_run.json', 'chainCd.sh', 'chainE.sh', 'extra-claim.log', 'collect_gates.py', 'wire-timing-ci-vs-head.txt', 'wire-8x8-vs-head.txt', 'verify-docs.err', 'verify-elab.err', 'verify-rtl.err', 'verify-rtlfast.err', 'started-AC.txt', 'started-BD.txt', 'sdk-install.log', 'sdk-install-docs.log']
copied = large = 0
def put(p, rel):
    global copied, large
    out = dst / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    if p.stat().st_size > LIMIT:
        with open(out.parent / 'large.sha256', 'a') as f:
            f.write(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.stat().st_size}  {out.name}\n')
        large += 1
    else:
        shutil.copy2(p, out)
        copied += 1
for name in TOP:
    if (src / name).is_file():
        put(src / name, name)
for root in ['rtl-fast', 'docs', 'elaborate', 'rtl', 'base-rtl', 'extra']:
    r = src / root
    for name in ['jobs.txt', 'driver.log']:
        if (r / name).is_file():
            put(r / name, f'{root}/{name}')
    for sub in ['logs', 'first-attempt-gptp', 'first-attempt-gates-1', 'cut-at-reset']:
        pass
    for sub in ['logs']:
        d = r / sub
        if d.is_dir():
            for p in sorted(d.iterdir()):
                if p.is_file():
                    put(p, f'{root}/{sub}/{p.name}')
print(copied, 'copied', large, 'over 200 KB by sha256')
