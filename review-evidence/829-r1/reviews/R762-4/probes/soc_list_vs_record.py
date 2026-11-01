#!/usr/bin/env python3
"""Compare the SoC's curated datapath source list with the record gate 1h reads: where the datapath and the macro's source sit.

usage: soc_list_vs_record.py <clone>
"""
import ast, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "syn/ooc"))
import dp_srcs
rec, _bad, _rc = dp_srcs.ask_authority("milan_datapath")
tree = ast.parse((root / "sw/litex/milan_soc.py").read_text())
node = next(n for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign)) and "_MILAN_DATAPATH_SOURCES" in
            [getattr(t, "id", None) for t in (n.targets if isinstance(n, ast.Assign) else [n.target])])
rows = []
for e in node.value.elts:
    if isinstance(e, ast.Constant) and isinstance(e.value, str): rows.append(e.value)
    else: rows.append("<" + ast.unparse(e) + ">")
rel = [str(Path(s).resolve().relative_to(root)) for s in rec["src"]]
dp, pkg = "hdl/milan/milan_datapath.sv", "hdl/common/ethernet_packet_pkg.sv"
print("soc literal rows", len(rows), "starred rows", [r for r in rows if r.startswith("<")])
print("soc: datapath row", rows.index(dp) if dp in rows else None, "pkg row", rows.index(pkg) if pkg in rows else None)
print("soc rows after the datapath:", rows[rows.index(dp) + 1:][:8] if dp in rows else None, "count", len(rows) - rows.index(dp) - 1 if dp in rows else None)
print("record: datapath at", rel.index(dp), "pkg source at", rel.index(pkg), "of", len(rel))
lit = [r for r in rows if not r.startswith("<")]
print("literal rows in the record", sum(r in rel for r in lit), "literal rows not in it", [r for r in lit if r not in rel][:8])
print("same order over the common literal rows:", [r for r in lit if r in rel] == [r for r in rel if r in lit])
