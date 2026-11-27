#!/usr/bin/env python3
"""Verify tracked bytes, Git modes, index and gitlinks without resetting files."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
head = git('rev-parse','HEAD').decode().strip()
tree = git('rev-parse','HEAD^{tree}').decode().strip()
index_tree = git('write-tree').decode().strip()
bad = []
files = []
links = []
for record in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not record:
        continue
    metadata,name = record.split(b'\t',1)
    mode,kind,oid = metadata.decode().split()
    path = root / os.fsdecode(name)
    if mode == '160000':
        links.append({'path':os.fsdecode(name),'oid':oid})
        continue
    data = os.fsencode(os.readlink(path)) if mode=='120000' else path.read_bytes()
    actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actual_mode = '120000' if path.is_symlink() else '100755' if path.stat().st_mode & stat.S_IXUSR else '100644'
    if actual != oid or actual_mode != mode:
        bad.append(os.fsdecode(name))
    files.append({'path':os.fsdecode(name),'blob':actual,'mode':actual_mode})
out = {'head':head,'tree':tree,'index_tree':index_tree,'tracked_files':len(files),'gitlinks':links,
       'byte_or_mode_mismatches':bad,'cached_diff':git('diff','--cached','--name-status').decode(),
       'worktree_diff':git('diff','--name-status').decode(),
       'round2_src_stat':git('diff','--stat','5d03517f','0f72ca69','--','src').decode(),
       'round2_src_include_diff':git('diff','5d03517f','0f72ca69','--','src','include').decode(),
       'tracked':files}
Path(__file__).with_name('integrity.json').write_text(json.dumps(out,indent=2)+'\n')
ok = head=='0f72ca69a0cd85ade9a3f1c42a325b23704cf625' and tree==index_tree=='6095ea2547e768550c65e717b9dd9b9450d764cb'
ok = ok and not bad and not out['cached_diff'] and not out['worktree_diff'] and not out['round2_src_include_diff']
print(json.dumps({'exact_head_tree_index':ok,'tracked_files':len(files),'gitlinks':links,'mismatches':bad}))
raise SystemExit(not ok)
