#!/usr/bin/env python3
"""plant_donor.py <clone> <donor mutant name>: apply the donor's own named
planted text (gptp-processor/tb/verilator/engine/mutants.py MUTATIONS,
RECEIPT_MUTATIONS or PARSER_EDITS) to the clone's gptp-processor checkout.
Each edit must match exactly once."""
import importlib.util, sys
from pathlib import Path
clone, name = Path(sys.argv[1]), sys.argv[2]
here = clone / "gptp-processor/tb/verilator/engine"
sys.path.insert(0, str(here))
spec = importlib.util.spec_from_file_location("donor_mutants", here / "mutants.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
table = {}
for n, rel, pat, rep, _c in mod.MUTATIONS + mod.RECEIPT_MUTATIONS:
    table[n] = ("gptp-processor/hdl/" + rel, mod.edits_of(pat, rep))
for n, edits in mod.PARSER_EDITS.items():
    table.setdefault(n, ("gptp-processor/hdl/wire/KL_gptp_rx_parser.sv", list(edits)))
if name not in table:
    sys.exit("REFUSED: no donor mutant named %r; known: %s" % (name, sorted(table)))
rel, edits = table[name]
path = clone / rel
text = path.read_text()
for old, new in edits:
    if text.count(old) != 1:
        sys.exit("REFUSED: %d occurrences of an edit in %s" % (text.count(old), rel))
    text = text.replace(old, new)
path.write_text(text)
print("planted %r in %s (%d edit(s))" % (name, rel, len(edits)))
