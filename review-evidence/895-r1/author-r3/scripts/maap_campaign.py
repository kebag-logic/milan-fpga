#!/usr/bin/env python3
"""maap_campaign.py TREE OUT: the control campaign (ctrl_mutants.campaign) of TREE, its table cut to the mutants a
change to the MAAP adapter or the mailbox driver can reach: those planted in maap/ or mbx/mbx.c, and those whose named
test is a MaapHost test or an F3b gate test; its own unnamed-test check runs as in the full campaign. Exit 1 when any
escaped or was refused."""
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree / 'sw/firmware/gtest'))
import ctrl_mutants  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

keep = tuple(m for m in ctrl_mutants.MUTANTS
             if m.path.startswith('maap/') or m.path == 'mbx/mbx.c' or m.test.startswith('MaapHost.')
             or '.F3b' in m.test)
print(f"{len(keep)} of {len(ctrl_mutants.MUTANTS)} mutants: {', '.join(m.name for m in keep)}", flush=True)
ctrl_mutants.MUTANTS = keep
out.mkdir(parents=True, exist_ok=True)
cut_reuse(out / 'reuse')
escaped = ctrl_mutants.campaign(out / 'mutants', out / 'reuse', 4)
print(f"maap campaign: {'FAIL' if escaped else 'PASS'}")
sys.exit(1 if escaped else 0)
