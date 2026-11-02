"""Probe the LiteX block census of docs/design/MARK_II_AREA_PLAN.md against the
LiteX-built objects sw/litex/milan_soc.py creates.

For each object: the line in milan_soc.py that builds it (proving it exists at
the head) and whether the census table names it. Prints one row per object.

Usage: python3 -I census_probe.py <clone>
Exit 0 always; the report is the evidence.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
soc = (root / "sw/litex/milan_soc.py").read_text(encoding="utf-8").splitlines()
page = (root / "docs/design/MARK_II_AREA_PLAN.md").read_text(encoding="utf-8")
census = page.split("### LiteX block census", 1)[1].split("### Console UART", 1)[0]

# (object, regex locating its construction in milan_soc.py, census keywords any of which names it,
#  build: basis = all-fabric shipping build, split = only under --ctrl-mailbox)
objects = [
    ("CPU wrapper", r"kwargs\[\"cpu_type\"\]\s*=\s*\"vexiiriscv\"", ["VexiiRiscvLitex_"], "basis"),
    ("_CRG", r"^class _CRG\(", ["_CRG"], "basis"),
    ("S7IDELAYCTRL", r"S7IDELAYCTRL\(", ["IDELAYCTRL"], "basis"),
    ("ddrphy A7DDRPHY", r"A7DDRPHY\(", ["ddrphy"], "basis"),
    ("sdram refresher", r"RegisteredRefresher", ["refresher"], "basis"),
    ("LiteSPI add_spi_flash", r"self\.add_spi_flash\(", ["LiteSPI"], "basis"),
    ("LiteEthPHYGMII", r"LiteEthPHYGMII\(", ["LiteEthPHYGMII"], "basis"),
    ("LiteEthMACCore", r"LiteEthMACCore\(", ["LiteEthMACCore"], "basis"),
    ("MAC TX PacketFIFO tx_sf", r"self\.tx_sf\s*=", ["TX FIFO"], "basis"),
    ("MDIO bit-bang", r"LiteEthPHYMDIO", ["MDIO"], "basis"),
    ("ICAPE2 reload port", r"Instance\(\"ICAPE2\"", ["ICAPE2"], "basis"),
    ("milan_mac.loopback CSRStorage", r"self\.loopback\s*=\s*CSRStorage", ["loopback"], "basis"),
    ("milan_mac.link_status CSRStorage (MAC_STATUS, REQ-MAC-03)", r"self\.link_status\s*=\s*CSRStorage",
     ["link_status", "link status", "MAC_STATUS"], "basis"),
    ("milan_axil_cdc", r"milan_axil_cdc\s*=", ["milan_axil_cdc"], "basis"),
    ("processor masters on dma_bus", r"_mem_bus\.add_master\(\"milan_desc_mem\"", ["dma_bus"], "basis"),
    ("ppmem observer", r"self\.ppmem\s*=\s*_PPMemDiag", ["ppmem"], "basis"),
    ("user_led identify", r"platform\.request\(\"user_led\", 0\)", ["user_led0"], "basis"),
    ("ctrl_memory (LiteX wishbone.SRAM banks, wishbone.Decoder)", r"bank = wishbone\.SRAM\(",
     ["ctrl_memory"], "split"),
    ("ctrl_mbx LiteX EventManager and CSR bank", r"soc\.csr\.add\(\"ctrl_mbx\"", ["ctrl_mbx"], "split"),
]
print("object | build | milan_soc.py line | census names it | census gives it a stage and fate")
for name, rx, keys, build in objects:
    line = next((i + 1 for i, s in enumerate(soc) if re.search(rx, s)), None)
    rows = [r for r in census.splitlines() if r.startswith("|") and any(k in r for k in keys)]
    named = bool(rows)
    as_block = any(r.split("|")[1].strip() and any(k in r.split("|")[1] for k in keys) for r in rows)
    fate_note = "as a block" if as_block else ("only as a fate or sub-part" if named else "no")
    print(f"{name} | {build} | {line} | {'yes' if named else 'NO'} | {fate_note}")
