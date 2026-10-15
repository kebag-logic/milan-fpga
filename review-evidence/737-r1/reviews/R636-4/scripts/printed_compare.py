#!/usr/bin/env python3
"""Compare each gate's printed output: unsharded log vs leg logs (reviewer-owned).

Usage: python3 -I printed_compare.py <ref.log> <leg0.log> <leg1.log>

A gate's block runs from its `test_name:` header line to the next header (or
the SUBSET / verdict lines).  Reports gates whose blocks are byte-identical,
identical after masking (scratch HOME and tree paths, /tmp names, decimal
seconds), and different.
"""
from __future__ import annotations

import re
import sys

HEADER = re.compile(r"^(test_[A-Za-z0-9_]+):$")
END = ("SUBSET:", "ALL GATES PASS", "\tCommand being timed", "Command exited")


def blocks(path: str) -> dict[str, list[str]]:
    out, current = {}, None
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines():
        m = HEADER.match(line)
        if m:
            current = m.group(1)
            out[current] = []
            continue
        if line.startswith(END) or re.match(r"^\d+ GATE ARM", line):
            current = None
            continue
        if current is not None:
            out[current].append(line)
    return out


def mask(lines: list[str]) -> list[str]:
    text = "\n".join(lines)
    text = re.sub(r"$REVIEWS/737-r636-4-packet/scratch/[A-Za-z0-9-]+", "<TREE>", text)
    text = re.sub(r"/tmp/[A-Za-z0-9_.-]+", "/tmp/<T>", text)
    text = re.sub(r"\btmp[a-z0-9_]{8}\b", "tmp<T>", text)
    text = re.sub(r"\d+\.\d+ ?s\b", "<S>s", text)
    text = re.sub(r"\b\d+(\.\d+)? seconds?\b", "<S> seconds", text)
    return text.splitlines()


def main() -> int:
    ref = blocks(sys.argv[1])
    legs: dict[str, list[str]] = {}
    for path in sys.argv[2:]:
        legs.update(blocks(path))
    same, masked, differ = [], [], []
    for gate, lines in ref.items():
        other = legs.get(gate)
        if other == lines:
            same.append(gate)
        elif other is not None and mask(other) == mask(lines):
            masked.append(gate)
        else:
            differ.append(gate)
    print(f"gates in reference: {len(ref)}; in legs: {len(legs)}")
    print(f"byte-identical: {len(same)}; identical after masking: {len(masked)}; different: {len(differ)}")
    print("masked:", ", ".join(masked))
    print("different:", ", ".join(differ))
    for gate in differ:
        a, b = mask(ref[gate]), mask(legs.get(gate, []))
        for x, y in zip(a, b):
            if x != y:
                print(f"  {gate}:\n    ref: {x[:300]}\n    leg: {y[:300]}")
                break
        else:
            print(f"  {gate}: line counts {len(a)} vs {len(b)}")
    return 1 if differ or set(ref) != set(legs) else 0


if __name__ == "__main__":
    raise SystemExit(main())
