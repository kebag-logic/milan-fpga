#!/usr/bin/env python3
"""R226-2: judge e2e CLI verdicts against the renderer oracle.

Usage: python3 -B e2e_vs_oracle.py <e2e-dir> <r226-1-e2e-oracle.json> <label>...

A copied label must be exempt exactly when the renderer shows the base
heading. E01-E18 use the R226-1 oracle (the page bytes come from the same
unchanged page() function); E19-E22 use e2e-oracle-new.json from this round.
A run whose CLI exited 2 judged no page, which is recorded as STOPPED.
"""
import json
import sys
from pathlib import Path

e2e, r1_oracle = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
oracle = dict(r1_oracle)
oracle.update(json.loads((e2e / "e2e-oracle-new.json").read_text()))
for label in sys.argv[3:]:
    res = json.loads((e2e / f"{label}-e2e.json").read_text())
    cli = res["_cli"]
    if cli["exit"] == 2:
        print(f"{label}: CLI exit 2, STOPPED before judging any page: {cli['summary']}")
        continue
    agree, escapes, withholds = 0, [], []
    for cid in sorted(k for k in res if not k.startswith("_")):
        rendered = all(v["old_heading_rendered"] for v in oracle[cid].values())
        hidden = not any(v["old_heading_rendered"] for v in oracle[cid].values())
        assert rendered or hidden, cid
        r = res[cid]
        exempt = not r["label_finding"] and not r["refusal_named"]
        if r["refusal_named"]:
            ok = True       # refused page: no exemption, named
        else:
            ok = exempt == rendered
        if ok:
            agree += 1
        elif exempt:
            escapes.append(cid)
        else:
            withholds.append(cid)
    print(f"{label}: CLI exit {cli['exit']}; {agree}/{agree + len(escapes) + len(withholds)} agree; "
          f"escapes {escapes}; withholds {withholds}; {cli['summary']}")
