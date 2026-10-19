#!/usr/bin/env python3
"""Independent split of the gate log's top-level [ok] lines: AECP defect names come from
the literal defect('<name>', ...) calls in aecp_mutants.py at the reviewed tree; pin
refusal lines start '[ok] lwSRP pin'. Usage: count_check.py <extract.log> <repo>"""
import re, sys
from pathlib import Path
log, repo = Path(sys.argv[1]), Path(sys.argv[2])
aecp = set(re.findall(r"defect\('([^']+)'", (repo / "sw/firmware/ctrl/test/aecp_mutants.py").read_text()))
ok = [l for l in log.read_text().splitlines() if l.startswith("[ok] ")]
pin = [l for l in ok if l.startswith("[ok] lwSRP pin")]
names = [l[5:].split(":", 1)[0] for l in ok]
aecp_hits = [n for n in names if n in aecp]
print("aecp_table_entries", len(aecp))
print("top_level_ok", len(ok))
print("pin_refusal_lines", len(pin))
print("lines_named_by_aecp_table", len(aecp_hits), "distinct", len(set(aecp_hits)))
print("aecp_names_without_ok", sorted(aecp - set(aecp_hits)))
print("763_mutants", [l for l in ok if "nvm-empty-map-keeps-defaults" in l or "nvm-unused-payload-reads-erased" in l])
print("ESCAPED_lines", sum("ESCAPED" in l for l in log.read_text().splitlines()))
