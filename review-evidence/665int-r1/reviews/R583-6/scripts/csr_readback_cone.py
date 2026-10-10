#!/usr/bin/env python3
"""R583-6 probe: does each CSR_READBACK input of milan_csr reach only the CSR bus's read data?

The census ends a cone at an input of the cell `csr` that CSR_READBACK names,
trusting that milan_csr routes those inputs to its read-back faces only.  This
probe elaborates milan_csr itself (the census's recipe and pinned sv2v/Yosys,
flattened, every process turned into cells, no optimisation) and follows each
of those inputs through every cell (each input bit to all output bits, a
memory's write to its reads) to the module outputs it reaches.

    csr_readback_cone.py TREE OUTDIR

TREE is a checkout of the head under review; SV2V and YOSYS name the pinned
tools.  Prints one line per input: the outputs its cone reaches.  Exit 0 when
every input reaches only the AXI read-data/read-response faces.
"""
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict, deque
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import census_elab as ce  # noqa: E402
import publication_census as pc  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
work = Path(tempfile.mkdtemp(prefix="csrcone-", dir=os.environ.get("TMPDIR")))
rcp = ce.recipe()
argv = ce.shadow(rcp, {}, work / "tree")
text = ce.run(argv, work, "sv2v")
(work / "all.v").write_text(text, encoding="utf-8")
ce.WORK.roms()
for rom in ce.WORK.path().iterdir():
    if rom.suffix == ".hex":
        (work / rom.name).write_bytes(rom.read_bytes())
ys = (f"read_verilog {work / 'all.v'}; hierarchy -check -top milan_csr; proc; flatten; "
      f"write_json {work / 'csr.json'}")
ce.run([ce.tool("yosys"), "-q", "-p", ys], work, "yosys")
doc = json.loads((work / "csr.json").read_text())
top = doc["modules"]["milan_csr"]
fan = defaultdict(list)
mem_rd = defaultdict(list)
cells = top["cells"]
for name, c in cells.items():
    t = c["type"]
    if t.startswith("$mem") and not t.startswith(("$memwr", "$meminit")):
        mem_rd[c["parameters"].get("MEMID", "")].append(name)
for name, c in cells.items():
    t = c["type"]
    dirs = c.get("port_directions", {})
    outs = [b for p, bits in c["connections"].items() if dirs.get(p) != "input" for b in bits if isinstance(b, int)]
    for p, bits in c["connections"].items():
        if dirs.get(p) == "output":
            continue
        for b in bits:
            if isinstance(b, int):
                if t.startswith(("$memwr", "$meminit")):
                    fan[b].append(("mem", c["parameters"].get("MEMID", "")))
                else:
                    fan[b].append(("bits", tuple(outs)))
outport = {}
for p, v in top["ports"].items():
    if v["direction"] != "input":
        for b in v["bits"]:
            if isinstance(b, int):
                outport.setdefault(b, set()).add(p)
lines, bad = [], 0
for port in sorted(pc.CSR_READBACK):
    start = [b for b in top["ports"][port]["bits"] if isinstance(b, int)]
    seen, todo, reached = set(start), deque(start), set()
    while todo:
        b = todo.popleft()
        reached |= outport.get(b, set())
        for kind, val in fan.get(b, ()):
            nxt = val if kind == "bits" else [o for r in mem_rd.get(val, ()) for p2, bs in cells[r]["connections"].items()
                                               if cells[r].get("port_directions", {}).get(p2) != "input" for o in bs
                                               if isinstance(o, int)]
            for o in nxt:
                if o not in seen:
                    seen.add(o)
                    todo.append(o)
    extra = sorted(reached - {"s_axi_rdata", "s_axi_rresp", "s_axi_rvalid"})
    bad += bool(extra)
    lines.append(f"[{'ok' if not extra else 'BAD'}] {port}: reaches {sorted(reached) or 'no output'}")
report = "\n".join(lines) + f"\ncsr read-back cone: {bad} of {len(pc.CSR_READBACK)} input(s) reach another output\n"
(out / "csr_readback_cone.txt").write_text(report, encoding="utf-8")
print(report, end="")
sys.exit(1 if bad else 0)
