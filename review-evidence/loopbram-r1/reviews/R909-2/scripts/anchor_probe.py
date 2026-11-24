#!/usr/bin/env python3
"""Reviewer anchor probe: every string literal in a mutation driver that matches
the RTL at the base must still match (or have a counterpart that matches) at the
head. Reports literals that anchored at base and anchor nowhere at head.

usage: anchor_probe.py <base-tree> <head-tree> <driver> [<driver> ...]
Drivers are repo-relative paths; RTL is every .sv/.v/.svh under hdl/ (both trees).
"""
import ast
import json
import sys
from pathlib import Path


def rtl(tree: Path) -> str:
    parts = []
    for p in sorted((tree / 'hdl').rglob('*')):
        if p.suffix in ('.sv', '.v', '.svh') and p.is_file():
            parts.append(p.read_text(errors='replace'))
    return '\n'.join(parts)


def literals(path: Path) -> list[str]:
    if not path.is_file():
        return []
    tree = ast.parse(path.read_text())
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 12:
            out.append(node.value)
    return out


def main() -> int:
    base, head = Path(sys.argv[1]), Path(sys.argv[2])
    rb, rh = rtl(base), rtl(head)
    report = []
    broken = 0
    for drv in sys.argv[3:]:
        lb = [s for s in literals(base / drv) if s in rb]
        lh = [s for s in literals(head / drv) if s in rh]
        lost = [s for s in lb if s not in rh and s not in lh]
        moved = [s for s in lb if s not in rh and s in lh]
        new = [s for s in lh if s not in lb]
        head_all = literals(head / drv)
        report.append(dict(driver=drv, base_anchors=len(lb), head_anchors=len(lh),
                           base_anchor_lost_at_head=len([s for s in lb if s not in rh]),
                           head_new_anchors=new, base_only_anchors=[s for s in lb if s not in rh]))
        # a lost anchor is acceptable only if the head driver carries a new anchor
        if len(lh) < len(lb):
            broken += 1
    print(json.dumps(report, indent=1))
    print('ANCHOR-DRIVERS-WITH-FEWER-ANCHORS', broken)
    return 1 if broken else 0


if __name__ == '__main__':
    raise SystemExit(main())
