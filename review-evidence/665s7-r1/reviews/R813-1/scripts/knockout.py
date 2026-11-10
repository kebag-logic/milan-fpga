#!/usr/bin/env python3
"""Reviewer knockout of srptx_grade.py: for each capture plant, a copy of the grader with that plant's own
check disabled must let the plant escape (its words absent). Also reports whether any other finding still
refuses the planted capture (overlap between checks), which is information, not a verdict.

  python3 -I knockout.py MILAN_DP_DIR CAPTURE_DIR WORK_DIR

WORK_DIR receives a disposable copy of the grader and plants; srp_wire_compare.py is imported from the
reviewed tree's sw/firmware/ctrl/test unchanged.
"""
import copy
import importlib
import json
import shutil
import sys
from pathlib import Path

DP, CAPS, WORK = (Path(a).resolve() for a in sys.argv[1:4])
ROOT = DP.parents[2]

#: plant -> (anchor in srptx_grade.py, its replacement): the plant's own check, disabled
KO = {
    "malformed-endmark": ('need(pdu[end - 2:end] == b"\\0\\0",', 'need(True or pdu[end - 2:end] == b"\\0\\0",'),
    "doubled-declaration": ("            if n > 1:", "            if False:"),
    "doubled-message": ("for kind in sorted({k for k in kinds if kinds.count(k) > 1}):", "for kind in []:"),
    "leave-all-wrong-type": ('if la and la != set(app["types"]):', "if False:"),
    "oversized": ("if length > MRPDU_MAX or 14 + length > FRAME_MAX:", "if False:"),
    "zero-source": ('for f in cap.mrpdus if f.frame[6:12].hex() != mac]', "for f in cap.mrpdus if False]"),
    "join-late": ("if until - f.us / 1000 > JOIN_FOLLOW_MS:", "if False:"),
    "join-late-in-t-svc": ("if until - f.us / 1000 > JOIN_FOLLOW_MS:", "if False:"),
    "rate": ("if (b.us - a.us) / 1000 < RATE_WINDOW_MS and not cap.held(a.ms, b.ms):", "if False:"),
    "leave-all-missing": ("elif gap > high or (f is not None and gap < low):", "elif False:"),
    "bench-overrun": ('if cap.doc["intra_ms_max_us"] >= MS_US:', "if False:"),
    "timer-layout": ('if cap.doc["layout_error"]:', "if False:"),
    "dropped-under-backpressure": ("while i < len(accepted) or j < len(sent):", "while False:"),
    "reordered": ("while i < len(accepted) or j < len(sent):", "while False:"),
    "backpressure-unseen": ('if not any(a <= r["ms"] < b for r in refused):', "if False:"),
    "refused-with-room": ('if r["ring_used"] + r["record"] <= words:', "if False:"),
    "retention-lost": ('if nxt is None or nxt["hex"] != r["hex"]:', "if False:"),
    "late-stop": ("if stop > deadline + SVC_MS or stop < deadline - RESOLUTION_MS:", "if False:"),
    "never-stopped": ('found.append(f"[608] the talker never stopped', '(lambda *a: None)(f"[608] the talker never stopped'),
    "stream-after-stop": ("        if late:", "        if False:"),
    "gate-not-licence": ('if p["gate"] & mask != licence & mask or p["active"] != p["admitted"] or p["active"] != p["gate"]:',
                         "if False:"),
    "aaf-without-licence": ('if p["aaf"] and not p["gate"] & 1:', "if False:"),
    "stream-without-licence": ("if not gate_at(policer, ms) and not gate_at(policer, ms - 1):", "if False:"),
}


def main():
    sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
    src = (DP / "srptx_grade.py").read_text()
    docs = {s: json.loads((CAPS / f"{s}.json").read_text()) for s in ("wire", "hold", "licence")}
    sys.path.insert(0, str(DP))
    import srptx_plants as sp
    missing = sorted(set(sp.PLANTS) - set(KO))
    bad = len(missing)
    for m in missing:
        print(f"FAIL {m}: no knockout written")
    for n, (name, (anchor, repl)) in enumerate(KO.items()):
        if src.count(anchor) != 1:
            print(f"FAIL {name}: anchor not once in srptx_grade.py")
            bad += 1
            continue
        d = WORK / f"ko{n:02d}"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        (d / "grade_ko.py").write_text(src.replace(anchor, repl))
        sys.path.insert(0, str(d))
        g = importlib.import_module("grade_ko")
        scenario, _, words = sp.PLANTS[name]
        doc = copy.deepcopy(docs[scenario])
        sp.plant(name, doc)
        p = d / "planted.json"
        p.write_text(json.dumps(doc) + "\n")
        clean = g.grade(g.load(CAPS / f"{scenario}.json"))[0]
        found = g.grade(g.load(p))[0]
        hit = [x for x in found if words in x]
        others = [x for x in found if x not in clean]
        ok = not hit
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: without its check the words {'still appear' if hit else 'are absent'}; "
              f"{len(others)} other new finding(s){': ' + others[0][:160] if others else ' (the plant escapes entirely)'}")
        sys.path.remove(str(d))
        del sys.modules["grade_ko"]
        shutil.rmtree(d, ignore_errors=True)
    print(f"knockouts: {len(sp.PLANTS) - bad} of {len(sp.PLANTS)} escape without their own check")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
