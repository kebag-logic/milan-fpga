#!/usr/bin/env python3
"""Seal completed receipts after all foreground test drivers have exited."""
from pathlib import Path
import hashlib, shutil, subprocess
P=Path(__file__).resolve().parents[1]
for n in range(4):
    assert (P/f'receipts/firmware/shard{n}.rc').read_text().strip()=='0'
assert (P/'receipts/checks/run-resume.rc').read_text().strip()=='0'
# The shard inventory writes these two temporary configurations in the checkout.
# Preserve them under scratch and remove only these known generated artifacts.
for name in ['keys-16x4.yaml','keys-16x32.yaml']:
    f=Path('dispatch-build/keys')/name
    if f.exists():
        target=P/'scratch/generated-inventory'/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(f),str(target))
for directory in [Path('dispatch-build/keys'),Path('dispatch-build')]:
    if directory.exists() and not any(directory.iterdir()):directory.rmdir()
with (P/'receipts/checks/tree-integrity.log').open('w') as out:
    subprocess.run(['python3',str(P/'scripts/verify_tree.py')],stdout=out,stderr=subprocess.STDOUT,check=True)
status=subprocess.check_output(['git','status','--porcelain=v1'],text=True)
assert not status,status
selected=[*sorted((P/'scripts').glob('*.py')),*sorted((P/'receipts').rglob('*'))]
selected += [P/'public/frozen-heads.json',P/'public/source-signatures.json',P/'public/pr945-findings-check.json',P/'public/pr945-head.json']
selected=[f for f in selected if f.is_file()]
with (P/'MANIFEST.sha256').open('w') as out:
    for f in sorted(set(selected)):
        out.write(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))+'\n')
report=(P/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R866] POSITIVE - exact head 732726660a88cd79a568d650d955d535fe79c720'
assert report.splitlines()[-1]=='R866-1 FINISHED' and 'SKELETON' not in report
print('PASS sealed',len(selected),'publishable files; exact tracked bytes/modes/index/gitlinks; clean worktree')
