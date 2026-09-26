#!/usr/bin/env python3
"""Disposable text probe: the parent's accepted port parser on tb/pp_top/pp_top_wrap.sv
at base, at head, and with the two new harness ports (and their //! contracts) moved
after dbg_notify_enq_o. Shows the head placement detaches the existing effect bundle
and that relocating the new ports alone restores it. No tracked file is modified."""
import subprocess, sys
from pathlib import Path
PK = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(PK / "scratch/parent-scripts"))
import check_port_contracts as ports  # noqa: E402
CLONE = "$REVIEWS/r334-1-pp120"
show = lambda rev: subprocess.run(["git", "-C", CLONE, "show", f"{rev}:tb/pp_top/pp_top_wrap.sv"],
                                  capture_output=True, text=True, check=True).stdout
base, head = show("0922e43408f891fc0b84a84691df86b4fd0f1c0d"), show("a9b7874d415d935949becd7ccfd58799927efb08")
start = head.index("    //! Processor event on clk_i: one cycle per accepted live 64-bit name")
end = head.index("    output logic        aecp_nvm_stb_o,")
block = head[start:end].rstrip("\n").rstrip() + "\n"
moved = head[:start] + head[end:]
tail = "    output logic        dbg_notify_enq_o\n);"
assert moved.count(tail) == 1
moved = moved.replace(tail, "    output logic        dbg_notify_enq_o,\n" + block.rstrip(",\n").rstrip(",") + "\n);")
for name, text in (("base", base), ("head", head), ("head, new ports moved after the bundle", moved)):
    total, undoc = ports.scan_ports(text)
    grp = [p for p in ("dbg_dyn_writes_o", "aecp_nvm_stb_o", "aecp_nvm_mark_o", "dbg_notify_enq_o",
                       "aecp_name_wr_o", "dbg_name_live_we_o") if p in undoc]
    print(f"{name}: ports {total}, undocumented {len(undoc)}; undocumented among effect/name ports: {grp}")
