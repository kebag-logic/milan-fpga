#!/usr/bin/env python3
"""Record bounded gate execution, unchanged scopes and final checkout integrity."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('packet',type=Path)
    a=ap.parse_args();root=a.root.resolve();packet=a.packet.resolve();r=packet/'receipts'
    records=[]
    for stem in ('docs-jobs','extra-docs-jobs'):
        records.extend(json.loads((r/(stem+'-results.json')).read_text()))
    assert len(records)==79 and all(v['rc']==0 for v in records)
    changed=subprocess.check_output(['git','diff','--name-only','c6bd08c6','HEAD'],cwd=root,text=True).splitlines()
    budgets=[s for s in changed if s.endswith('.budget')]
    firmware=[s for s in changed if s.startswith('sw/firmware/')]
    gitlinks=subprocess.check_output(['git','diff','--raw','c6bd08c6','HEAD'],cwd=root,text=True)
    assert not budgets
    assert firmware==['sw/firmware/ctrl/aecp/README.md']
    assert not any(s.startswith(':160000') or ' 160000 ' in s for s in gitlinks.splitlines())
    result=dict(executed_commands=len(records),all_returned_zero=True,records=records,
                changed_budgets=budgets,changed_firmware=firmware,changed_gitlinks=[],
                prohibited_not_executed=['full builder bank','act orchestrator/selftest'],
                timestamp_utc=datetime.now(timezone.utc).isoformat())
    (r/'docs-census.json').write_text(json.dumps(result,indent=2)+'\n')
    moved=[]
    for rel in ('scripts/__pycache__','sw/builder/out'):
        source=root/rel
        if not source.exists():continue
        assert not subprocess.check_output(['git','ls-files','--',rel],cwd=root),rel
        dest=packet/'scratch/checkout-generated'/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        assert not dest.exists(),dest
        shutil.move(str(source),str(dest));moved.append(rel)
    (r/'generated-output-relocation.json').write_text(json.dumps(dict(
        moved=moved,destination='scratch/checkout-generated',
        reason='Documentation gates generated ignored outputs in the checkout; moved to scratch after completion.'),indent=2)+'\n')
    data=subprocess.check_output(['python3',str(packet/'scripts/verify_checkout.py'),str(root)])
    (r/'checkout-verification.json').write_bytes(data)
    verify=json.loads(data);assert verify['status']=='' and verify['ignored']==[]
    group=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split(':',2)[2].lstrip('/')
    resource={name:(group/name).read_text().strip() for name in ('memory.max','memory.peak','memory.events')}
    (r/'resource-use.json').write_text(json.dumps(resource,indent=2)+'\n')
    print(json.dumps(dict(docs_commands=len(records),all_zero=True,changed_budgets=budgets,
                         changed_firmware=firmware,moved_ignored=moved,checkout_clean=True,
                         resources=resource),indent=2))

if __name__=='__main__':main()
