"""report_compare.py AUTHOR_RECEIPT_DIR OBJ_SRPTX: each scenario's report (obj_srptx/<s>-report.json) against the
author's published receipt <s>-report.json.txt (its JSON after the '---' line): equal findings and measured
blocks. The receipt's first lines are a header; the JSON starts at the first line that is '{'."""
import json, sys
from pathlib import Path
a, o = Path(sys.argv[1]), Path(sys.argv[2])
for s in ("wire", "hold", "licence"):
    text = (a / f"{s}-report.json.txt").read_text().splitlines()
    theirs = json.loads("\n".join(text[text.index("{"):] if "{" in text else text[next(i for i, l in enumerate(text) if l.startswith("{")):]))
    mine = json.loads((o / f"{s}-report.json").read_text())
    keys = sorted(set(theirs) | set(mine))
    print(s, "keys", keys)
    for k in keys:
        print(f"  {k}: {'equal' if theirs.get(k) == mine.get(k) else 'DIFFERENT'}")
