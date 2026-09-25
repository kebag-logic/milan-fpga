#!/usr/bin/env python3
"""Disposable-tree only: add milan_csr as one more OOC top in syn/yosys/ooc.sh.
usage: ooc-add-csr.py <tree>"""
import pathlib, sys
p = pathlib.Path(sys.argv[1]) / "syn/yosys/ooc.sh"
t = p.read_text()
anchor = '  "milan_datapath|$DP_SRCS"\n'
assert t.count(anchor) == 1
p.write_text(t.replace(anchor, anchor + '  "milan_csr|$R/hdl/common/csr/milan_csr.sv"\n'))
