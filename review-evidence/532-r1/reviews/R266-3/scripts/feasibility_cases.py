#!/usr/bin/env python3
"""Scratch-only feasibility probe for R266-3 F1-F3: extra stand-in faults and cases.

Usage: feasibility_cases.py PROOF_SCRIPT OUT_SCRIPT
Writes a copy of PROOF_SCRIPT whose stand-ins gain one-slot faults and whose
self-test gains five cases. Each edit must apply exactly once. It is evidence
that deterministic cases for the surviving mutants exist; it is not a patch
proposed for the tree, and the tree's file is only read.
"""
import pathlib
import sys

EDITS = [
    # F1: a leak in one slot only; the stand-in nsenter knows which slot it entered.
    ('def answers(specs, inside):\n',
     'def answers(specs, inside, slot=None):\n'),
    ('reached = alive and f"slot-reaches-{name}" in faults and (name, host, port) in known',
     'reached = alive and (f"slot-reaches-{name}" in faults or f"slot{slot}-reaches-{name}" in faults) '
     'and (name, host, port) in known'),
    ('answers(args[args.index("-c") + 2:], inside=True)',
     'answers(args[args.index("-c") + 2:], inside=True, slot=slot)'),
    # F2: the network query fails after removal.
    ('    elif verb == "network ls":\n',
     '    elif verb == "network ls" and "network-query-fails" in faults:\n'
     '        sys.exit("docker: Cannot connect to the Docker daemon (stand-in)")\n'
     '    elif verb == "network ls":\n'),
    # F3: one slot never announces its daemon; run B refused after announcing, before A holds.
    ('    if "slot-unannounced" not in faults:\n',
     '    if "slot-unannounced" not in faults and f"slot{slot}-unannounced" not in faults:\n'),
    ('if slot == "2" and "refused-while-held" in faults:\n',
     'if slot == "1" and "b-refused-while-held" in faults:\n'
     '    for _ in range(600):\n'
     '        if (state / "b-refused-while-held").exists():\n'
     '            break\n'
     '        time.sleep(0.05)\n'
     'if slot == "2" and "refused-while-held" in faults and "b-refused-while-held" not in faults:\n'),
    ('    if pr == "21" and slot == "1" and run_number == 1 and "refused-while-held" in faults:\n',
     '    if pr == "23" and slot == "2" and run_number == 1 and "b-refused-while-held" in faults:\n'
     '        print("act-ci: REFUSED: action clone failed", file=sys.stderr, flush=True)\n'
     '        (state / "b-refused-while-held").touch()\n'
     '        sys.exit(2)\n'
     '    if pr == "21" and slot == "1" and run_number == 1 and "refused-while-held" in faults:\n'),
    # The five cases.
    ('the isolation target cannot be queried after removal|target-query-fails|23|1|FAIL isolation target not proved absent\n',
     'the isolation target cannot be queried after removal|target-query-fails|23|1|FAIL isolation target not proved absent\n'
     'probe: only slot B reaches the container|slot2-reaches-container|23|1|FAIL isolation slot 2\n'
     'probe: the isolation network cannot be queried after removal|network-query-fails|23|1|FAIL isolation target not proved absent\n'
     'probe: run B is refused before slot A is taken|b-refused-while-held|23|1|FAIL overlap\n'
     'probe: only slot A never reports its daemon|slot1-unannounced|23|1|FAIL overlap\n'
     'probe: only slot B never reports its daemon|slot2-unannounced|23|1|FAIL overlap\n'),
]


def main() -> int:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            print(f"edit applies {count} times: {old[:70]!r}", file=sys.stderr)
            return 2
        text = text.replace(old, new, 1)
    pathlib.Path(sys.argv[2]).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
