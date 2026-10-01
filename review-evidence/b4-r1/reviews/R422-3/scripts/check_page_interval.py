#!/usr/bin/env python3
"""Check the #451 timing page's talker-to-unbind interval against the packet, on one clock.

usage: check_page_interval.py <page.md> <runs/timing-long dir>
Reads the interval the page states ("N.N s before the unbind, on the controller
host's clock"), computes it from the controller host's own stamps (talker
`end` record in controller-logs.txt, first record of ctl-unbind.jsonl), and
exits 0 only if the page value equals the single-clock interval rounded to
0.1 s and the page names the controller host's clock. Exit 1 otherwise.
"""
import json, os, re, sys
page, d = sys.argv[1], sys.argv[2]
text = " ".join(open(page).read().split())
m = re.search(r"talker also ended ([\d.]+) s before the unbind(, on the controller host's clock)?", text)
if not m:
    print("page: interval sentence not found"); sys.exit(1)
stated, named = float(m.group(1)), bool(m.group(2))
end = None
for l in open(os.path.join(d, "controller-logs.txt")):
    if l.startswith("{"):
        r = json.loads(l)
        if r.get("kind") == "end":
            end = r["t"]
unbind = json.loads(open(os.path.join(d, "ctl-unbind.jsonl")).readline())["t"]
ev = {e.get("tag", e["kind"]): e["t"] for e in map(json.loads, open(os.path.join(d, "events.jsonl")))}
single = unbind - end
mixed = ev["unbind"] - end
ok = named and abs(stated - round(single, 1)) < 1e-9
print(json.dumps(dict(page_stated_s=stated, page_names_controller_clock=named,
                      single_clock_s=round(single, 3), mixed_clocks_s=round(mixed, 3),
                      verdict="AGREE" if ok else "DISAGREE"), indent=1))
sys.exit(0 if ok else 1)
