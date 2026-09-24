"""R272-6 closure probe: round four's scripts/r5/cases_r5_closure.py, whose
Part A stops on its own `== 2520` assertion at a head whose table holds 6440
cells, re-run with that one number lifted and nothing else changed. Its
functions (gcc_keeps, s_verdict, reader) and its Part B BOUNDARY/EXTRA
templates are IMPORTED from the unchanged round-four file, not copied.

Run inside gate 1b's own namespace by scripts/r1/probe_gate1b.py (anchor:
accepted); grades no firmware, returns no cases.

Part A: every cell of the head's `_closure_corpus()` (all 23 positions),
GCC's answer taken HERE by one direct `gcc -std=gnu99 -E -P` per cell, then
compared with `_CLOSURE_KEPT`, with S's verdict and with the gate's readers.
Part B: round four's boundary table, unchanged.
Part C: for each of the fourteen round-five positions, the table cells are
matched by (template, X) to round four's Part B rows (receipt
R272_PARTB_PREV) and to this run's Part B rows: same text, same GCC answer,
same S verdict class, same reader answer.

Environment: R272_GCC, R272_OUT, R272_R5_SCRIPT (path of the unchanged
cases_r5_closure.py), R272_PARTB_PREV (round four's partB-boundary.json).
"""
import importlib.util
import json
import os
from pathlib import Path


def _r5():
    spec = importlib.util.spec_from_file_location(
        "r272_r5_closure", os.environ["R272_R5_SCRIPT"])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cases(ns):
    r5 = _r5()
    import test_builder as mod
    gcc = os.environ["R272_GCC"]
    out = Path(os.environ["R272_OUT"])
    out.mkdir(parents=True, exist_ok=True)
    outcomes = mod._LEXER_OUTCOMES
    cells = [(label, text, rd) for label, text, rd, _o in
             mod._closure_corpus()]
    assert len(cells) == len(mod._CLOSURE_KEPT) == 6440, len(cells)
    per = len(cells) // len(mod._CLOSURE_POSITIONS)
    measured = r5.gcc_keeps(gcc, [t for _l, t, _r in cells])
    counts = {"allowlist": 0, "other": 0, "admitted": 0,
              "recorded_vs_gcc_mismatch": 0, "admitted_disagree": 0,
              "allowlist_reader_differs": 0}
    rows, disagree = [], []
    for index, ((label, text, rd), letter, (found, _stdout)) in enumerate(
            zip(cells, mod._CLOSURE_KEPT, measured)):
        recorded = outcomes[letter]
        verdict = r5.s_verdict(ns, text)
        read = r5.reader(ns, rd, text)
        kind = verdict.split(":")[0]
        counts[kind] += 1
        if found != recorded:
            counts["recorded_vs_gcc_mismatch"] += 1
        if kind == "admitted" and read != found:
            counts["admitted_disagree"] += 1
            disagree.append(label)
        if kind == "allowlist" and read != found:
            counts["allowlist_reader_differs"] += 1
        rows.append({"cell": label, "position": index // per, "S": verdict,
                     "reader": read, "gcc": found, "recorded": recorded})
    (out / "partA-closure-6440.json").write_text(
        json.dumps({"counts": counts, "admitted_disagree": disagree,
                    "rows": rows}, indent=0, default=str) + "\n",
        encoding="utf-8")
    print("PART A", json.dumps(counts), disagree, flush=True)
    # Part B, round four's own code path, unchanged templates
    spelled = [(f"byte 0x{b:02x}", bytes([b])) for b in range(256)]
    for seq in mod._CLOSURE_SEQUENCES:
        try:
            spelled.append((f"U+{ord(seq.decode('utf-8')):04X}", seq))
        except UnicodeDecodeError:
            spelled.append(("bytes " + seq.hex(" "), seq))
    xs = spelled + [("extra " + (s.hex(" ") or "EMPTY"), s) for s in r5.EXTRA]
    bcells = []
    for where, template, in_code in r5.BOUNDARY:
        for name, seq in xs:
            bcells.append((f"{name} | {where}", template.replace(
                "{X}", seq.decode("utf-8", errors="surrogateescape")),
                in_code))
    bmeasured = r5.gcc_keeps(gcc, [t for _l, t, _c in bcells])
    brows = {}
    bcounts = {"allowlist": 0, "other": 0, "admitted": 0,
               "admitted_disagree": 0}
    for (label, text, _c), (found, _stdout) in zip(bcells, bmeasured):
        verdict = r5.s_verdict(ns, text)
        read = r5.reader(ns, "keeps", text)
        kind = verdict.split(":")[0]
        bcounts[kind] += 1
        if kind == "admitted" and read != found:
            bcounts["admitted_disagree"] += 1
        brows[text] = {"cell": label, "S": kind, "reader": read,
                       "gcc": found}
    print("PART B", len(bcells), "cells", json.dumps(bcounts), flush=True)
    # Part C: the fourteen new positions against both Part B runs
    prev = {}
    for row in json.loads(Path(os.environ["R272_PARTB_PREV"]).read_text(
            encoding="utf-8"))["rows"]:
        prev[row["cell"]] = row
    templates = {t: w for w, t, _c in r5.BOUNDARY}
    c = {"new_cells": 0, "template_in_round4_partB": 0,
         "same_as_this_partB": 0, "same_as_round4_partB": 0, "differ": []}
    for row, (label, text, rd) in zip(rows, cells):
        if row["position"] < 9:
            continue
        c["new_cells"] += 1
        template = mod._CLOSURE_POSITIONS[row["position"]][1]
        if template not in templates:
            c["differ"].append(["template not in round four's Part B", label])
            continue
        c["template_in_round4_partB"] += 1
        mine = brows.get(text)
        kind = row["S"].split(":")[0]
        now = (kind, row["reader"], row["gcc"])
        if mine and (mine["S"], mine["reader"], mine["gcc"]) == now:
            c["same_as_this_partB"] += 1
        else:
            c["differ"].append(["this Part B", label, now, mine])
        name = label[:-len(" " + mod._CLOSURE_POSITIONS[row["position"]][0])]
        # the table names a non-UTF-8 string "bytes .. (not UTF-8)", round
        # four's Part B "bytes .."
        name = name.removesuffix(" (not UTF-8)")
        old = prev.get(f"{name} | {templates[template]}")
        oldnow = None if old is None else (
            old["S"].split(":")[0],
            None if old["reader"] is None else tuple(old["reader"]),
            None if old["gcc"] is None else tuple(old["gcc"]))
        if oldnow == now:
            c["same_as_round4_partB"] += 1
        else:
            c["differ"].append(["round four Part B", label, now, oldnow])
    (out / "partC-new-cells-vs-partB.json").write_text(
        json.dumps(c, indent=1, default=str) + "\n", encoding="utf-8")
    print("PART C", json.dumps({k: v for k, v in c.items() if k != "differ"}),
          "differ", len(c["differ"]), c["differ"][:5], flush=True)
    return ()
