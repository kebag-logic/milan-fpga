#!/usr/bin/env python3
"""Per-file first-party port counts of one tree, as check_port_contracts.audit() counts them.

usage: python3 -I port_census.py <repo>   (prints "<tree>\t<file>\t<ports>" per file)
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import check_port_contracts as c  # noqa: E402

for rel in c.sources():
    n, _u = c.scan_ports((c.REPO / rel).read_text(errors="replace"))
    print(f"{c.tree_of(rel)}\t{rel}\t{n}")
