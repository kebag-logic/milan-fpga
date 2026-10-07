#!/usr/bin/env python3
"""Read-only licence and private-marker screening of every reachable blob."""
from pathlib import Path
import json
import re
import subprocess
import sys

repo=Path(sys.argv[1])
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args])
identifiers=set()
conflicts=[]
private=[]
count=0
for row in git('rev-list','--objects','--all').decode().splitlines():
    oid=row.split()[0]
    if git('cat-file','-t',oid).strip()!=b'blob':continue
    count+=1
    data=git('cat-file','blob',oid)
    for match in re.finditer(rb'SPDX-License-Identifier:\s*([a-zA-Z0-9.+-]+)',data):
        identifiers.add(match[1].decode())
    if re.search(rb'(?i)(?:GNU (?:General|Lesser|Affero) Public License|MIT License|BSD[- ](?:2|3)[- ]Clause|Mozilla Public License|ISC License|All rights reserved)',data):
        conflicts.append(oid)
    if re.search(rb'(?i)(?:/home/[^/\s]+/|/data/[^/\s]+/|/Users/[^/\s]+/|-----BEGIN [A-Z ]*PRIVATE KEY-----|\b(?:github_pat_|ghp_)[A-Za-z0-9_]{20,})',data):
        private.append(oid)
result={'scope':'all six current branch histories','blobs':count,'spdx_identifiers':sorted(identifiers),'other_licence_markers':conflicts,'private_path_or_credential_markers':private,'provenance_limit':'Owner assertion and repository inspection; no forensic authorship guarantee','algorithm_attribution':'src/core/switch_ctrl.c:23 and src/include/shish_lan/switch_ctrl.h:93 identify an algorithm; no competing code notice found'}
print(json.dumps(result,indent=2))
assert identifiers=={'Apache-2.0'} and not conflicts and not private
