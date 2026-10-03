#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 6): are the mutants probe_r6_lists.py found surviving exit-equivalent at head, or gaps?

Copies of the committed baseline, each with one edit, go through check-baseline with the head's gate and with the
mutated copies probe_r6_lists.py left under <lists-scratch>. The head's exit status is what the documented class
requires; a mutant giving the same status on every case here is exit-equivalent on these inputs, and one that
differs on a case is a test gap that case would close.

Usage: probe_r6_equiv.py <checkout> <lists-scratch> <scratch-dir>
"""

import json
from pathlib import Path
import subprocess
import sys

REPO, LISTS, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
SCRATCH.mkdir(parents=True, exist_ok=True)
COMMITTED = (REPO / "syn/ooc/pp_resource_baseline.json").read_text()
COUNTS = None
WIDE_SCOPE = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.:/-[]" * 2)[:128]


def scopes_of(tree: dict) -> dict:
    return tree["endpoints"]["route-1x1"]["record"]["scopes"]


def add_scope(name: str):
    def apply(tree: dict) -> None:
        scopes = scopes_of(tree)
        scopes[name] = dict(next(iter(scopes.values())))
    return apply


def put(path: tuple, value: object):
    def apply(tree: dict) -> None:
        held = tree
        for key in path[:-1]:
            held = held[key]
        held[path[-1]] = value
    return apply


CASES = {
    # label: (edit, the exit status the documented class implies)
    "committed baseline unchanged": (lambda tree: None, 0),
    "scope name of 128 characters holding every SCOPE_NAME character": (add_scope(WIDE_SCOPE), 0),
    "scope name with upper case, u_PP/Core": (add_scope("u_PP/Core"), 0),
    "scope name with a colon, u_pp:core": (add_scope("u_pp:core"), 0),
    "scope name with a hyphen, u_pp-core": (add_scope("u_pp-core"), 0),
    "scope name of 128 characters, x * 128": (add_scope("x" * 128), 0),
    "note: key in a list inside a list, description [[{x[1]: 1}]]": (put(("description",), [[{"x[1]": 1}]]), 2),
    "note: key in the fourth list item, description [{}, {}, {}, {x[1]: 1}]":
        (put(("description",), [{}, {}, {}, {"x[1]": 1}]), 2),
    "note: two refused keys in items 0 and 1, description [{a b: 1}, {x[1]: 1}]":
        (put(("description",), [{"a b": 1}, {"x[1]": 1}]), 2),
    "note: record-shaped below endpoints at depth 5, description {endpoints: {x: {record: {scopes: {a[1]: 1}}}}}":
        (put(("description",), {"endpoints": {"x": {"record": {"scopes": {"a[1]": 1}}}}}), 2),
    "record figures: bracketed key LUT[0]": (put(("endpoints", "route-1x1", "record", "figures", "LUT[0]"), 1), 2),
    "record identity: bracketed key tool[0]":
        (put(("endpoints", "route-1x1", "record", "identity", "tool[0]"), "x"), 2),
    "measured note: record-shaped, {record: {scopes: {a[1]: 1}}} at endpoints/route-1x1/measured":
        (put(("endpoints", "route-1x1", "measured"), {"record": {"scopes": {"a[1]": 1}}}), 2),
}
GATES = {"head": REPO / "syn/ooc"} | {folder.name: folder for folder in sorted(LISTS.iterdir())
                                      if folder.is_dir() and folder.name != "control"}


def main() -> None:
    paths = {}
    for index, (label, (apply, _)) in enumerate(CASES.items()):
        tree = json.loads(COMMITTED)
        apply(tree)
        paths[label] = SCRATCH / f"case{index:02d}.json"
        paths[label].write_text(json.dumps(tree, indent=1))
    differs: dict[str, list[str]] = {}
    for label, (apply, want) in CASES.items():
        row = []
        for gate, folder in GATES.items():
            done = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "check-baseline",
                                   "--baseline", str(paths[label]), "--budget",
                                   str(REPO / "docs/design/AREA_BUDGET.md")], cwd=REPO, capture_output=True, text=True,
                                  timeout=600)
            row.append(f"{gate}={done.returncode}")
            if gate == "head":
                head = done.returncode
                reason = (done.stdout + done.stderr).strip().splitlines()[-1:] or [""]
                print(f"{'ok ' if head == want else 'BAD'} head rc={head} want={want}: {label} [{reason[0][:110]}]")
            elif done.returncode != head:
                differs.setdefault(gate, []).append(f"{label}: head {head}, mutant {done.returncode}")
    print()
    for gate in GATES:
        if gate != "head":
            print(f"{'DIFFERS ' if gate in differs else 'same    '} {gate}" +
                  "".join(f"\n           {line}" for line in differs.get(gate, [])))


if __name__ == "__main__":
    main()
