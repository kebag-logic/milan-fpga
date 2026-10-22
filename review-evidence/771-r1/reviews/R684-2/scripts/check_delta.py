#!/usr/bin/env python3
"""Check the review delta and unchanged production/oracle inputs. Usage: check_delta.py REPO"""
import hashlib
from pathlib import Path
import re
import subprocess
import sys
root=Path(sys.argv[1])
def git(*args): return subprocess.check_output(['git','-C',str(root),*args])
old='a97aea01449492b1f640924f5a34726f602cabed'
head='1098978f4a931a667e147b68a791520eb141c917'
print(git('log','--format=%H %s',old+'..'+head).decode())
print(git('diff','--stat',old+'..'+head).decode())
for path in ('hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv','hdl/milan/milan_datapath.sv','hdl/milan/KL_pp_shadow.sv'):
    before=git('show',old+':'+path).decode()
    after=git('show',head+':'+path).decode()
    # Only whole-line comments changed in these particular hunks.
    strip=lambda s: '\n'.join(x for x in s.splitlines() if not x.lstrip().startswith('//'))
    assert strip(before)==strip(after),path
    print('RTL behavior bytes unchanged after removing whole-line comments:',path)
for path in ('protocol-processor','gptp-processor','third_party/tsn-c-stack','sw/firmware/ctrl/app','sw/firmware/ctrl/test/ctrl_reuse.py'):
    assert not git('diff',old,head,'--',path),path
    print('Unchanged:',path)
path='sw/firmware/milan_baremetal/milan_baremetal.c'
data=git('show',head+':'+path)
assert data==git('show','d77a8afd:'+path)
print('Shipping firmware SHA256:',hashlib.sha256(data).hexdigest())
diff=git('diff','--unified=0',old,head,'--','*.sv','*.cpp','*.py').decode()
added=[x for x in diff.splitlines() if x.startswith('+') and not x.startswith('+++')]
residue=[x for x in added if re.search(r'\b(?:lane|round|reviewer|B\d\d|R68[34])\b|issuecomment-',x,re.I)]
assert not residue,residue
print('New source-comment provenance residue scan: none')
assert not git('diff','--check','d77a8afd',head)
print('Whitespace check: PASS')
