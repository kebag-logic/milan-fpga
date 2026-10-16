#!/usr/bin/env python3
"""Presence-only identity check; never prints the identifier.
Usage: privacy.py REPOSITORY AUTHOR_PACKET PR_JSON OUTPUT_PACKET
The repository must contain the public round-1 commit.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

repo, packet, pr, out = map(Path, sys.argv[1:])
old = subprocess.check_output(['git','-C',str(repo),'show',
    '18b98bbcecf478b903610a07667f232d944d6feb:docs/findings/387_SOFTWARE_GM_STEP.md'],text=True)
identities = re.findall(r'[0-9a-f]{16}', old.splitlines()[444])
assert len(identities) == 1
value = identities[0]
forms = [value, ':'.join(value[i:i+2] for i in range(0,16,2)),
         '-'.join(value[i:i+2] for i in range(0,16,2)),
         value[:6]+'.'+value[6:10]+'.'+value[10:],
         ':'.join(value[i:i+4] for i in range(0,16,4))]
result = {}
for role, root in [('docs',repo/'docs'),('published_packet',packet)]:
    hits = []
    for file in sorted(root.rglob('*')):
        if file.is_file():
            text = file.read_text(errors='replace').lower()
            if any(form in text for form in forms):
                hits.append(str(file.relative_to(root)))
    result[role] = hits
body = json.loads(pr.read_text())['body'].lower()
result['pr_body_present'] = any(form in body for form in forms)
(out/'privacy-check.json').write_text(json.dumps(result,indent=2)+'\n')
assert not result['docs'] and not result['pr_body_present']
print('Repository docs and PR body: no identity in five equivalent forms. Published packet matches: '+str(len(result['published_packet'])))
