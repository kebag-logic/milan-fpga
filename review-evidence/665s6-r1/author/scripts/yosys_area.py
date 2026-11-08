#!/usr/bin/env python3
"""yosys_area.py <tree> <shape> <split 0|1> <out.json> - a Yosys LUT/FF ESTIMATE of milan_datapath (#665 S6).

A measurement, not a gate: the census's recipe (sw/mailbox/census_elab.py) for the shape (its header, the builder's
parameters), CTRL_SPLIT_P bound as given, every source lowered by the pinned sv2v, then the pinned Yosys's
`synth_xilinx -family xc7 -flatten` and `stat -tech xilinx -json`, the method of syn/yosys/ooc.sh (flatten first, so
a cell inside a submodule is counted). Writes the stat record and a LUT/FF/BRAM summary.

`<shape>` "mbx" measures the split SoC's mailbox side instead: KL_mbx and KL_mbx_cdc, each flattened on its own.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

tree, shape_name, split, out = Path(sys.argv[1]).resolve(), sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
sys.path[:0] = [str(tree / "sw/mailbox")]
import census_elab as ce  # noqa: E402

MBX = ["hdl/milan/mailbox/KL_mbx_pkg.sv", "hdl/milan/mailbox/KL_mbx_ring.sv", "hdl/milan/mailbox/KL_mbx_rx.sv",
       "hdl/milan/mailbox/KL_mbx_tx.sv", "hdl/milan/mailbox/KL_mbx_evt.sv", "hdl/milan/mailbox/KL_mbx.sv",
       "hdl/common/cdc_handshake.sv", "hdl/common/cdc_pulse.sv", "hdl/milan/mailbox/KL_mbx_cdc_window.sv",
       "hdl/milan/mailbox/KL_mbx_cdc.sv"]


def summary(stat: dict, top: str) -> dict:
    cells = stat["modules"].get(f"\\{top}", stat["modules"].get(top, {})).get("num_cells_by_type", {})
    lut = sum(n for t, n in cells.items() if re.fullmatch(r"\$?_*LUT[1-6]_*", t.strip("\\")) or t.startswith("LUT"))
    ff = sum(n for t, n in cells.items() if re.match(r"FD[CPRSE]", t.strip("\\")))
    bram = {t: n for t, n in cells.items() if "RAMB" in t}
    lutram = {t: n for t, n in cells.items() if re.match(r"RAM\d|RAM\d+[MX]", t.strip("\\"))}
    srl = sum(n for t, n in cells.items() if "SRL" in t)
    dsp = sum(n for t, n in cells.items() if "DSP" in t)
    return {"LUT": lut, "FF": ff, "BRAM": bram, "LUTRAM": lutram, "SRL": srl, "DSP": dsp}


def synth(srcs: list[Path], incdirs: list[Path], defines, top: str, params, work: Path) -> dict:
    text = ce.run([ce.tool("sv2v"), *(f"-D{d}" for d in defines), *(a for d in incdirs for a in ("-I", str(d))),
                   *map(str, srcs)], work, "sv2v refused")
    (work / "all.v").write_text(text)
    bind = "".join(f" -chparam {k} {v}" for k, v in params)
    script = (f"read_verilog -defer {work / 'all.v'}; hierarchy -check -top {top}{bind}; "
              f"synth_xilinx -family xc7 -flatten -top {top}; tee -q -o {work / 'stat.json'} stat -tech xilinx -json")
    t0 = time.time()
    subprocess.run([ce.tool("yosys"), "-q", "-p", script], cwd=work, check=True, stdout=subprocess.DEVNULL,
                   stderr=open(work / "yosys.err", "w"))
    stat = json.loads((work / "stat.json").read_text())
    return {"top": top, "params": dict(params), "seconds": round(time.time() - t0), **summary(stat, top),
            "cells_by_type": stat["modules"].get(f"\\{top}", stat["modules"].get(top, {})).get("num_cells_by_type")}


work = Path(tempfile.mkdtemp(prefix="yosys-area-", dir="$VALIDATION_STORAGE/665s6-a745"))
try:
    ce.toolchain()
    ce.WORK.roms()
    for _g, image in ce.ROMS:
        shutil.copy(ce.WORK.path() / image, work / image)
    if shape_name == "mbx":
        rows = [synth([tree / f for f in MBX], [], (), t, (), work) for t in ("KL_mbx", "KL_mbx_cdc")]
        record = {"tree_head": subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], capture_output=True,
                                              text=True).stdout.strip(), "shape": "mbx", "rows": rows}
    else:
        shape = next(s for s in ce.shapes() if s.name == shape_name)
        rcp = ce.shaped(ce.recipe(), shape)
        params = (*shape.params, ("CTRL_SPLIT_P", split)) if split else shape.params
        row = synth([Path(s).resolve() for s in rcp.sources], [Path(d).resolve() for d in rcp.incdirs],
                    rcp.defines, ce.TOP, params, work)
        record = {"tree_head": subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], capture_output=True,
                                              text=True).stdout.strip(), "shape": shape_name, "split": split, **row}
    out.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "cells_by_type"}, sort_keys=True)[:600])
finally:
    shutil.rmtree(work, ignore_errors=True)
