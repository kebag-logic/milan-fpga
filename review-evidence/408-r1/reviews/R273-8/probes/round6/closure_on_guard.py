#!/usr/bin/env python3
"""R273-8: does gate 1b's own assert_directive_set_is_closed() (loaded
unmodified, as delta_probe.py loads it) refuse each null-directive case of
cases/round6/null-directive-more.json, independent of which rule the full
gate reports first? usage: closure_on_guard.py <repo> <cases.json>"""
import json, sys
from pathlib import Path
here = Path(__file__).resolve().parent
src = (here / "delta_probe.py").read_text().replace("\nsys.exit(main())\n", "\n")
d = {"__file__": str(here / "delta_probe.py"), "__name__": "d"}
exec(compile(src, "delta_probe.py", "exec"), d)
ns = d["load"](Path(sys.argv[1]))
for case in json.loads(Path(sys.argv[2]).read_text()):
    try:
        ns["assert_directive_set_is_closed"](case["firmware"])
        said = "PASSES the directive-set closure"
    except AssertionError as exc:
        said = "REFUSED by the directive-set closure: " + str(exc)[:110]
    print(case["label"][:60], "|", said)
