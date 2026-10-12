#!/usr/bin/env python3
"""Lane B16, round 2: a neutral, public receipt of the tone source's read-only meter and state reads.

usage: r2_source_b16.py <class-map.json> <reads.json> <out-receipt.json>

The reads themselves (the source's control-service messages, observed passively, with one
documented state request in a state read) name the source's controls and stay outside the packet.
So does the class map, which says which controls are meters, which meter belongs to which role,
and which neutral class a state entry belongs to. Their SHA-256 are in the receipt, and the reads
are listed in RAW-ARTIFACTS.json; nothing in the receipt names a control, an address, a channel
number or a clock value.

<reads.json>: {"reads": [{"label", "path", "kind": "meters"|"state"}], "compare": [[label, label], ...]}

For every read: its time (CEST, from the read's own start time), size withheld, SHA-256 and
message count. For every meter role the map names: per channel of the role, the number of
readings, and the median, minimum and maximum of the level leaving the source and, for an
output, of the level before its level setting (the first and third value of each reading, dBFS);
readings at minus infinity are counted but not in those figures. For every other output only the
largest reading of either kind, so that the output count stays withheld. For every state read:
its entries (the last value of each address that is not a meter) and the output level settings the
map names, per role. For every compared pair: the entries each holds, the entries both hold, the
entries that differ, and per differing entry its neutral class, how many messages for that
address each read caught, whether each read's last value is among the messages the other caught,
and for a monitoring-mix entry whether every one of those messages is at minus infinity.
"""
import datetime
import hashlib
import json
import math
import re
import statistics
import sys
from pathlib import Path

CEST = datetime.timezone(datetime.timedelta(hours=2))


def main() -> int:
    cmap_p, reads_p, out_p = map(Path, sys.argv[1:4])
    cmap = json.loads(cmap_p.read_text())
    spec = json.loads(reads_p.read_text())
    meter = re.compile(cmap["meter"])
    roles = [(r["role"], [re.compile(x) for x in r["channels"]]) for r in cmap["meter_roles"]]
    other = re.compile(cmap["other_outputs"]) if cmap.get("other_outputs") else None
    settings = [(r["role"], [re.compile(x) for x in r["channels"]]) for r in cmap.get("level_settings", [])]
    classes = [(c["class"], re.compile(c["match"]), c.get("mix", False)) for c in cmap["entry_classes"]]

    out = dict(tool="r2_source_b16.py", class_map_sha256=hashlib.sha256(cmap_p.read_bytes()).hexdigest(),
               reads={}, compare=[])
    msgs, last = {}, {}
    for r in spec["reads"]:
        p = Path(r["path"])
        b = p.read_bytes()
        d = json.loads(b)
        ms = d["msgs"]
        msgs[r["label"]] = ms
        lst = {}
        for m in ms:
            if not meter.search(m["addr"]):
                lst[m["addr"]] = m["args"]
        last[r["label"]] = lst
        rec = dict(kind=r["kind"], at=datetime.datetime.fromtimestamp(d["t0"], CEST).strftime("%H:%M:%S"),
                   bytes="withheld: it would state the source's control layout",
                   sha256=hashlib.sha256(b).hexdigest(), messages=len(ms))
        lv = {}
        for role, chans in roles:
            per = []
            for rx in chans:
                v = [m["args"] for m in ms if rx.fullmatch(m["addr"])]
                fin = [a for a in v if isinstance(a[0], float) and a[0] > -math.inf]
                pre = [a for a in fin if len(a) >= 5 and isinstance(a[2], float)]
                per.append(dict(readings=len(v),
                                leaving_dbfs=None if not fin else [round(statistics.median(a[0] for a in fin), 2),
                                                                   round(min(a[0] for a in fin), 2), round(max(a[0] for a in fin), 2)],
                                before_setting_dbfs=None if not pre else [round(statistics.median(a[2] for a in pre), 2),
                                                                          round(min(a[2] for a in pre), 2), round(max(a[2] for a in pre), 2)]))
            lv[role] = per
        if other is not None:
            ov = [m["args"] for m in ms if other.fullmatch(m["addr"]) and not any(rx.fullmatch(m["addr"]) for _, cs in roles for rx in cs)]
            def top(vals):
                f = [x for x in vals if isinstance(x, float) and x > -math.inf]
                return round(max(f), 2) if f else "minus infinity"
            lv["every other output"] = dict(readings="withheld: it would state the source's output count",
                                            largest_leaving_dbfs=top(x for a in ov for x in a[:2]),
                                            largest_before_setting_dbfs=top(x for a in ov for x in a[2:4]))
        if r["kind"] == "meters" or any(p["readings"] for v in lv.values() if isinstance(v, list) for p in v):
            rec["meters"] = lv
        if r["kind"] == "state":
            rec["entries"] = len(lst)
            rec["level_settings_db"] = {role: [(lst.get(next((a for a in lst if rx.fullmatch(a)), ""), [None]) or [None])[0]
                                               for rx in chans] for role, chans in settings}
        out["reads"][r["label"]] = rec

    for a, b in spec["compare"]:
        la, lb = last[a], last[b]
        common = sorted(set(la) & set(lb))
        diff = []
        for k in (k for k in common if la[k] != lb[k]):
            cls, mix = next(((c, m) for c, rx, m in classes if rx.fullmatch(k)), ("other", False))
            va = [m["args"] for m in msgs[a] if m["addr"] == k]
            vb = [m["args"] for m in msgs[b] if m["addr"] == k]
            e = dict(cls=cls, messages=[len(va), len(vb)],
                     first_last_among_second=la[k] in vb, second_last_among_first=lb[k] in va)
            if mix:
                e["all_minus_infinity"] = all(x[0] == -math.inf for x in va + vb)
            diff.append(e)
        out["compare"].append(dict(first=a, second=b, entries=[len(la), len(lb)], both=len(common),
                                   differ=len(diff), differing=sorted(diff, key=lambda e: e["cls"])))
    out_p.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps([dict(pair=[c["first"], c["second"]], entries=c["entries"], both=c["both"], differ=c["differ"])
                      for c in out["compare"]]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
