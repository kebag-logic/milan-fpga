"""Usage: python3 -B crosscheck_probe.py <clone>
In-process probe of gen_mailbox.crosscheck on the 32x32 layout: (a) as generated, (b) the wrapping bound
restored on the ACMP transmit ring, (c) the event ring's upper bound dropped (a decode overrunning its ring).
Prints each finding list; edits no file."""
import sys
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / "sw/mailbox"))
import gen_mailbox as g
contract = g.load()
variant, sources, sinks = g.shape_variant(contract, clone / "configs/endstation_ax7101_32x32.yaml", 2)
texts = g.generate(variant)
top = "hdl/milan/mailbox/KL_mbx.sv"
print("(a) as generated:", g.crosscheck(variant, texts))
old = ("  assign acmp_tx_host_w = wr_w && off_w >= AW2_C'(MBX_CH_ACMP_TX_BASE_C);   "
       "//! the ring ends at the window's top")
new = ("  assign acmp_tx_host_w = wr_w && off_w >= AW2_C'(MBX_CH_ACMP_TX_BASE_C)\n                      "
       "&& off_w < AW2_C'(MBX_CH_ACMP_TX_BASE_C + 4 * MBX_CH_ACMP_TX_WORDS_C);")
print("(b) wrapping bound:", g.crosscheck(variant, g._plant(texts, top, old, new)))
old = ("  assign evt_host_w = rd_w && off_w >= AW2_C'(MBX_EVT_BASE_C)\n"
       "                      && off_w < AW2_C'(MBX_EVT_BASE_C + 4 * MBX_EVT_WORDS_C);")
new = "  assign evt_host_w = rd_w && off_w >= AW2_C'(MBX_EVT_BASE_C);"
print("(c) event ring unbounded above:", g.crosscheck(variant, g._plant(texts, top, old, new)))
