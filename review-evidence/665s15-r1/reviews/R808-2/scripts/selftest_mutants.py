"""Usage: python3 -B selftest_mutants.py <clone> <mutant>
Runs gen_mailbox.selftest() with one in-process mutant; edits no file. Mutants:
  unsized   - acmp_tx_words returns the layout's own ring (no sizing from the rule)
  norefuse  - shape_findings' short-ring refusal removed
  bounded   - the skeleton bounds every ring above, the window's top included (the pre-fix decode)"""
import sys
from pathlib import Path
clone = Path(sys.argv[1]).resolve(); which = sys.argv[2]
sys.path.insert(0, str(clone / "sw/mailbox"))
import gen_mailbox as g
import mailbox_skeleton as sk
if which == "unsized":
    g.acmp_tx_words = lambda c, sinks: next(ch for ch in c.channels if ch.name == "acmp").tx_words
elif which == "norefuse":
    orig = g.shape_findings
    g.shape_findings = lambda v, so, si: [f for f in orig(v, so, si) if "PROBE_TX_COMMANDs" not in f]
elif which == "bounded":
    orig_rd = sk._ring_decode
    sk._ring_decode = lambda c, host, access, base, words, end: orig_rd(c, host, access, base, words, -1)
rc = g.selftest()
print(f"MUTANT {which}: selftest rc {rc} ({'caught' if rc else 'NOT CAUGHT'})")
