"""Usage: python3 -B window_probe.py <clone> <tmpdir>
Does the contract loader accept a window that is not a power of two (0x7800, the contract's rings and blocks
unchanged)? If it does, what upper bound does the skeleton give a ring ending at that window's top, and what
width is the decode? Edits no tracked file."""
import sys
from dataclasses import replace
from pathlib import Path
clone = Path(sys.argv[1]).resolve(); tmp = Path(sys.argv[2])
sys.path.insert(0, str(clone / "sw/mailbox"))
import gen_mailbox as g
import mailbox_model as m
text = m.CONTRACT.read_text(encoding="utf-8")
p = tmp / "mailbox.yaml"; p.write_text(text.replace("window_bytes: 0x8000", "window_bytes: 0x7800"), encoding="utf-8")
try:
    c = m.load(p)
    print("window 0x7800: accepted by load(); ADDR_W bits", (c.window_bytes // 4 - 1).bit_length())
except m.ContractError as e:
    print("window 0x7800: refused by load():", e); sys.exit(0)
try:
    v = g.with_tx_ring(c, "acmp", 512)
    ch = next(x for x in v.channels if x.name == "acmp")
    print(f"acmp tx ring 512 words placed at {ch.tx_base:#x}, ends {ch.tx_base + 4 * ch.tx_words:#x}")
    top = g.generate(v)["hdl/milan/mailbox/KL_mbx.sv"]
    print([l for l in top.splitlines() if "acmp_tx_host_w =" in l])
    print("crosscheck:", g.crosscheck(v, g.generate(v)))
except Exception as e:
    print("placement/generation:", type(e).__name__, e)
# The ring placed by hand at the 0x7800 window's top: 0x7000..0x7800, if the layout leaves it free.
try:
    v = replace(c, channels=tuple(replace(x, tx_base=0x7000, tx_words=512) if x.name == "acmp" else x for x in c.channels))
    m._check_contract(v)
    top = g.generate(v)["hdl/milan/mailbox/KL_mbx.sv"]
    print("at the top:", [l.strip() for l in top.splitlines() if "acmp_tx_host_w =" in l])
    print("decode width bits:", ((v.window_bytes // 4 - 1).bit_length() + 2), "so offsets 0x7800..0x7ffc also satisfy it")
    print("crosscheck:", g.crosscheck(v, g.generate(v)))
except Exception as e:
    print("at the top:", type(e).__name__, e)
