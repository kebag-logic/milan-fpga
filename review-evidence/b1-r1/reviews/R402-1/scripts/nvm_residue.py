#!/usr/bin/env python3
"""Compare the DUT's saved-state (NVM) console line and PP_STAT between the identity gate
and the final restore console. usage: nvm_residue.py <packet-root: .../review-evidence/b1-r1>"""
import re, sys
from pathlib import Path
au = Path(sys.argv[1]) / "author"
for label, f in [("identity gate", au / "identity/console-identity.txt"), ("final restore", au / "restore/console-final.txt")]:
    t = f.read_text()
    pp = re.search(r"PP_STAT=([0-9a-f]{8})", t)[1]
    nvm = re.findall(r"^NVM: .*$", t, re.M)
    print("%s (%s): PP_STAT=%s PP_STAT[11]=%d" % (label, f.relative_to(au), pp, (int(pp, 16) >> 11) & 1))
    for l in nvm:
        print("   " + l)
