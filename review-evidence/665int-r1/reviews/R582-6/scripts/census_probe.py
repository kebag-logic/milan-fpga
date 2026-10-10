#!/usr/bin/env python3
"""census_probe.py - run the publication census of a checkout on planted copies of its front-end files.

Usage:
  python3 census_probe.py REPO [--shape NAME] [--edit PATH OLD NEW]... [--label TEXT]

Each edit names a file the front end reads (relative to REPO); its OLD text
must occur exactly once. The edits are handed to the census as an overlay
(nothing in REPO is written), the census elaborates the planted copy at the
named shape (the recipe's by default) and prints every finding. Exit 0 when
the census accepts the copy, 1 when it refuses it, 2 when it cannot read it.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("--shape", default="recipe")
    ap.add_argument("--edit", nargs=3, action="append", default=[], metavar=("PATH", "OLD", "NEW"))
    ap.add_argument("--label", default="probe")
    args = ap.parse_args()
    sys.path.insert(0, str(args.repo / "sw/mailbox"))
    import census_elab as ce
    import mailbox_model
    import publication_census as pc
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    overlay: dict[Path, str] = {}
    for path, old, new in args.edit:
        old, new = old.encode().decode("unicode_escape"), new.encode().decode("unicode_escape")
        f = (args.repo / path).resolve()
        text = overlay.get(f) or f.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"[{args.label}] REFUSED: the old text occurs {text.count(old)} times in {path}")
            return 2
        overlay[f] = text.replace(old, new)
    shape = next(s for s in ce.shapes() if s.name == args.shape)
    known = pc.fields(mailbox_model.load())
    print(f"[{args.label}] {ce.toolchain()}; shape {shape.name}; planted {', '.join(p for p, _, _ in args.edit) or 'nothing'}")
    try:
        base = pc.overlay(src)
        base.update(overlay)
        net = ce.elaborate(base, shape)
        out, svs = pc.census(src, pc.CENSUS, known, (shape,), 1, {shape.name: net})
    except ce.CensusError as exc:
        print(f"[{args.label}] the census cannot read it: {exc}")
        return 2
    sv = svs[0]
    print(f"[{args.label}] {sv.size}; {len(sv.reads)} read(s), {len(sv.unread)} unread")
    for f in out:
        print(f"[{args.label}] FINDING {f}")
    print(f"[{args.label}] {'REFUSED' if out else 'ACCEPTED'} ({len(out)} finding(s))")
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
