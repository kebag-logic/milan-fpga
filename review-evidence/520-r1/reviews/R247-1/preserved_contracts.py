#!/usr/bin/env python3
"""Compare gate policies and inventory to the source commit's actual parent."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
base='483a133ed08867ea0d300d2b4a027b5b48a4282f'
def git(*args):return subprocess.check_output(['rtk','proxy','git','-C',str(root),*args])
before=git('show',base+':syn/yosys/run.sh').decode()
after=(root/'syn/yosys/run.sh').read_text()
rows={}
for name in ['derive_sources','build_inventory','select_tops','require_tools','prepare_tmp','record_result','run_tops','report','main']:
    pattern=r'^'+name+r'\(\) \{.*?^\}'
    a=re.search(pattern,before,re.M|re.S).group();b=re.search(pattern,after,re.M|re.S).group()
    assert a==b,name
    rows[name]=hashlib.sha256(a.encode()).hexdigest()
for name in ['scripts/yosys_tally.py','scripts/yosys_shards.py','.github/workflows/rtl.yml','.github/workflows/rtl-fast.yml','syn/yosys/malloc.sh','syn/yosys/check_tap_purity.sh','scripts/check_tied_inputs.sh']:
    data=(root/name).read_bytes();assert data==git('show',base+':'+name),name
    rows[name]=hashlib.sha256(data).hexdigest()
rows['changed_paths']=git('diff','--name-only',base,'HEAD').decode().splitlines()
assert len(rows['changed_paths'])==6
inventory=subprocess.check_output(['rtk','proxy','bash',str(root/'syn/yosys/run.sh'),'--list'],cwd=root)
assert len(inventory.decode().splitlines())==54
assert inventory==(out/'public-evidence/review-evidence/520-r1/author/inventory-before.txt').read_bytes()
rows['top_count']=54;rows['inventory_sha256']=hashlib.sha256(inventory).hexdigest()
(out/'preserved-contracts.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS: source/tool/program/stat/structural/inventory/workflow identities preserved')
