#!/usr/bin/env python3
"""Elaborate the composed tree's CtrlMailbox (sw/litex/milan_soc.py) with migen and
emit it as Verilog, so its two Instances can be bound to the mailbox RTL by a
separate lint step.

Usage: python3 probe_ctrl_mailbox.py <candidate clone> <output .v>
Run with an interpreter that imports migen + litex; writes nothing but <output .v>.
"""
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw" / "litex"))
import milan_soc  # noqa: E402  (the composed file, M2 and the publication ports)
from migen.fhdl.verilog import convert  # noqa: E402

contract = milan_soc.ctrl_mailbox_contract()
mbx = milan_soc.CtrlMailbox(100_000_000, contract)
b = mbx.bus
ios = {b.cyc, b.stb, b.we, b.adr, b.dat_w, b.sel, b.ack, b.dat_r, b.err, mbx.ev.mbx.trigger}
text = str(convert(mbx, ios=ios, name="probe_ctrl_mailbox"))
out.write_text(text, encoding="utf-8")
inst = [ln.strip() for ln in text.splitlines() if ln.strip().startswith(("KL_mbx", ".pub_"))]
print(f"interfaces={contract.interfaces} pub_sources={contract.pub_sources} "
      f"pub_sinks={contract.pub_sinks}")
print("\n".join(inst))
