#!/usr/bin/env python3
"""Audit the immutable public packet. Usage: audit_packet.py SOURCE."""
from pathlib import Path
import gzip
import hashlib
import json
import re
import subprocess as sp
import sys
root=Path(__file__).resolve().parent
source=Path(sys.argv[1]).resolve()
rev='9330a4a9f596d8914d9f52ebf426147568d8b438'
prefix='review-evidence/948-r1/'
def show(path):
    return sp.check_output(['git','-C',str(source),'show',rev+':'+prefix+path])
manifest=json.loads(show('MANIFEST.json'))
bad=[]
for e in manifest:
    if hashlib.sha256(show(e['file'])).hexdigest()!=e['published_sha256']: bad.append(e['file'])
commit=sp.check_output(['git','-C',str(source),'cat-file','commit',rev]).decode()
author=[e for e in manifest if e['file'].startswith('author-r3/')]
with (root/'packet-audit.txt').open('w') as f:
    f.write(f'Public packet commit {rev}\nManifest entries checked: {len(manifest)}; mismatches: {len(bad)}\nRound-three author entries: {len(author)}\nEmbedded commit signature: {"present" if "gpgsig " in commit else "absent"}\n')
    f.write('Hashes verify published bytes, not cryptographic signer authentication.\n')
assert not bad,bad
base='author-r3/receipts/'
with (root/'published-fit-audit.txt').open('w') as f:
    for shape in ('1x1','8x8'):
        for directive in ('ExtraPostPlacementOpt','ExtraTimingOpt','AltSpreadLogic_high'):
            p=base+'fit/'+shape+'-'+directive+'/'
            f.write('\n'+shape+' '+directive+'\n')
            for item in ('recipe.txt','build.rc','identity.log','signoff.txt','utilization.txt','baseline-provenance.txt'):
                f.write(item+'\n'+show(p+item).decode()+'\n')
    f.write('\nSource identity:\n'+show(base+'gates/source-identity.txt').decode())
with (root/'published-gates-audit.txt').open('w') as f:
    for rel in ('rtl/avtp_rxmon-suite-64117b77.log.gz','sweep/milan_dp-64117b77-excerpt.txt.gz','sweep/milan_dp_mclk-SUMMARY-64117b77.txt','sweep/small-suites-SUMMARY-64117b77.txt','twin/twin-gate-64117b77.log.gz','gates/gates-64117b77.txt','rtl/dt5-plant/result.txt'):
        data=show(base+rel)
        text=(gzip.decompress(data) if rel.endswith('.gz') else data).decode()
        f.write('\nARTIFACT '+base+rel+'\n')
        for line in text.splitlines():
            if re.search(r'checks|failures|RESULT|rc=|finding|PASS|FAIL|SKIP|NOT RUN|caught|END|head|64117',line) and not re.search(r'^\[PASS\].*input \d|^\[PASS\].*octets|^\[PASS\].*FAN',line):
                f.write(line+'\n')
        f.write('LAST LINES\n'+'\n'.join(text.splitlines()[-8:])+'\n')
print((root/'packet-audit.txt').read_text())
