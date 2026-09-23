#!/usr/bin/env python3
"""Independent literal-record audit for issue 439 (reviewer-owned).

Usage: python3 verify_records.py <repo-root>

Enumerates the scope from the issue text, not from the checker: the seven
RTL jobs named by CI_WORKFLOWS item 4 plus full-ci-gate's step named
"Print the event and pin the one SHA this run validates". Normalizes each
live run body with an independent shell-style normalizer and compares it to
the record the checker holds at the same position. Also reports whether the
record object is a literal tuple of str, and that no out-of-scope entry
gained a run record. Exit 0 only when every scoped body matches.
"""
import importlib.util
import pathlib
import re
import sys

import yaml

SEVEN = {
    ".github/workflows/rtl.yml": ("verilator-shards", "verilator-suites",
                                  "yosys-shards", "yosys-portability"),
    ".github/workflows/rtl-fast.yml": ("verilator-lint", "bdd-conformance",
                                       "yosys-elaboration"),
}
SHA_STEP = "Print the event and pin the one SHA this run validates"


def norm(text):
    text = text.replace("\\\n", "")
    out = []
    for raw in text.split("\n"):
        line = " ".join(w for w in re.split(r"[ \t]+", raw) if w)
        if line:
            out.append(line)
    return out


def main(root):
    root = pathlib.Path(root)
    spec = importlib.util.spec_from_file_location(
        "ci_events_under_review", root / "scripts" / "ci_events.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pins = mod.RTL_SEQUENCE_PINS
    bad, scripts, lines_total = [], 0, 0
    scoped = []
    for rel, jids in SEVEN.items():
        wf = yaml.safe_load((root / rel).read_text())
        for jid in jids:
            for at, step in enumerate(wf["jobs"][jid]["steps"]):
                if "run" in step:
                    scoped.append((rel, jid, at, step))
    wf = yaml.safe_load((root / ".github/workflows/rtl.yml").read_text())
    for at, step in enumerate(wf["jobs"]["full-ci-gate"]["steps"]):
        if step.get("name") == SHA_STEP:
            scoped.append((".github/workflows/rtl.yml", "full-ci-gate", at, step))
    for rel, jid, at, step in scoped:
        key = (rel, jid)
        entry = pins[key][at]
        rec = entry.get("run")
        live = norm(step["run"])
        literal = isinstance(rec, tuple) and rec and all(isinstance(x, str) for x in rec)
        same = literal and list(rec) == live
        scripts += 1
        lines_total += len(live)
        status = "MATCH" if same else "MISMATCH"
        print(f"{status} {jid} step {at + 1} `{step.get('name')}` "
              f"lines={len(live)} literal_tuple={bool(literal)} "
              f"entry_name_match={entry.get('name') == step.get('name')}")
        if not same:
            bad.append((jid, at + 1, live, rec))
    # No out-of-scope entry may have gained a run record in this change.
    out_of_scope = []
    for (rel, jid), entries in pins.items():
        for at, entry in enumerate(entries):
            in_scope = (jid in SEVEN.get(rel, ())) or (
                jid == "full-ci-gate" and entry.get("name") == SHA_STEP)
            if not in_scope and "run" in entry and jid != "physical-gptp":
                out_of_scope.append((jid, at + 1, entry.get("name")))
    print(f"scripts={scripts} normalized_lines={lines_total}")
    print(f"out_of_scope_run_records(excluding physical-gptp)={out_of_scope}")
    for b in bad:
        print("DETAIL", b)
    return 0 if not bad and scripts == 38 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
