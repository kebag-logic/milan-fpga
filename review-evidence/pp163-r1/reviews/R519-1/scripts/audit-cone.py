#!/usr/bin/env python3
"""Reconcile public endpoint families; this is not a fresh synthesis traversal."""
from collections import Counter
import json,pathlib,re
p=pathlib.Path(__file__).resolve().parents[1];pub=p/"receipts/public";records={}
for revision in ("base","head"):
 lines=(pub/f"arbiter-standalone-levels-{revision}.tsv").read_text().splitlines()
 cells={line.split("\t")[2].rsplit("/",1)[0] for line in lines}
 groups=Counter(re.sub(r"\[\d+\]","[*]",cell) for cell in cells)
 assert len(cells)==188 and groups.pop("sof_pend_r_reg")==1
 # The public parent wrapper connects tx_sof_o to nothing, so this single
 # otherwise-unused register is absent from the integrated measurement.
 summary=(pub/("cone-summary-base-over20.txt" if revision=="base" else "cone-summary-head-all.txt")).read_text()
 observed=set(re.findall(r"-> u_tx_arbiter/(\S+):",summary))
 assert set(groups)==observed,(revision,set(groups)-observed,observed-set(groups))
 records[revision]={"integrated_cells":sum(groups.values()),"families":dict(sorted(groups.items())),"all_families_present":True,"summary_header":summary.splitlines()[0]}
 assert sum(groups.values())==187
records["limit"]="The public packet describes the start/end-pair traversal but does not include its Tcl or full integrated TSVs. This inventory reconciliation does not execute or verify that traversal."
(p/"receipts/cone-inventory-audit.json").write_text(json.dumps(records,indent=2)+"\n");print(json.dumps(records,indent=2))
