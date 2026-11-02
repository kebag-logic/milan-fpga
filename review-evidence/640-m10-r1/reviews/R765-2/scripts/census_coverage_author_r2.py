"""Map every LiteX-built object of the basis build, and every LiteX part the
split build adds, to one row of the LiteX block census in
docs/design/MARK_II_AREA_PLAN.md, and fail if any object has no row.

Usage:
    python3 -I census_coverage.py <repo> <litex.log tree excerpt> <csr.csv> <hierarchical_place.rpt>

Sources of the objects:
  - the basis build's SoC hierarchy (litex.log): every depth-0 node, and every
    depth-1 node under cpu, crg, milan and milan_mac;
  - the basis build's csr.csv: every csr_register and csr_base;
  - the basis build's placed hierarchy: every child of the CPU wrapper;
  - sw/litex/milan_soc.py at the head: the LiteX parts only the split build
    (--ctrl-mailbox) builds.
Each object maps by an explicit rule to a census row key; the key must occur
in the first (block) cell of exactly one census row. rc 1 on any miss.
"""
import re
import sys
from pathlib import Path

repo, tree_path, csr_path, rpt_path = (Path(a) for a in sys.argv[1:5])
page = (repo / "docs/design/MARK_II_AREA_PLAN.md").read_text(encoding="utf-8")
census = page.split("### LiteX block census", 1)[1].split("### Console UART", 1)[0]
rows = [r for r in census.splitlines() if r.startswith("| ") and not r.startswith("| Block today")]
blocks = [r.split("|")[1] for r in rows]
soc = (repo / "sw/litex/milan_soc.py").read_text(encoding="utf-8")

# census row keys: a string that occurs in that row's block cell
ROW = {
    "cpu": "CPU wrapper",
    "irq": "Interrupt controller",
    "crg": "Clock and reset generation",
    "idelay": "`idelay` clock",
    "ctrl": "`ctrl` (`SoCController`)",
    "ident": "Identifier `identifier_mem`",
    "timer": "`timer0`",
    "uart": "UART (`RS232PHY`",
    "spi": "SPI flash",
    "eth": "Ethernet MAC and PHY",
    "mdio": "MDIO (`LiteEthPHYMDIO`)",
    "macfp": "`MilanMAC`'s first-party parts",
    "link": "`link_status` CSR",
    "loop": "`loopback` CSR",
    "bus": "SoC bus and CSR interconnect",
    "axilcdc": "`milan_axil_cdc`",
    "pp": "The processor's memory paths",
    "ddr": "DDR3:",
    "bios_rom": "BIOS ROM `rom`",
    "bios_sram": "BIOS SRAM `sram`",
    "led": "LEDs or GPIO",
    "ctrlmem": "`ctrl_memory`",
    "ctrlmbx": "`ctrl_mbx`'s LiteX parts",
}

# (source, object, rule) -> row
RULES_TREE0 = {
    "bus": "bus", "csr": "bus", "irq": "irq", "ctrl": "ctrl", "cpu": "cpu", "dma_bus": "pp",
    "rom": "bios_rom", "sram": "bios_sram", "identifier": "ident", "uart": "uart",
    "timer0": "timer", "crg": "crg", "ddrphy": "ddr", "sdram": "ddr",
    "litedramaxi2native_0": "ddr", "spiflash": "spi", "milan_mac": "eth", "milan": "axilcdc",
    "descmem_fsm": "pp", "respmem_fsm": "pp", "nvmmem_fsm": "pp", "ppmem": "pp",
    "csr_bridge": "bus", "csr_bankarray": "bus", "csr_interconnect": "bus",
}
RULES_TREE1 = {
    ("cpu", "soc_bus"): "bus", ("cpu", "memory_port_cdc0"): "ddr", ("cpu", "memory_port_stage0"): "ddr",
    ("cpu", "[BB:VexiiRiscvLitex_"): "cpu",
    ("crg", "pll"): "crg", ("crg", "idelayctrl"): "idelay", ("crg", "[BB:PLLE2_ADV]"): "crg",
    ("crg", "[BB:MMCME2_ADV]"): "crg", ("crg", "[BB:BUFG]"): "crg",
    ("milan", "milan_axil_cdc"): "axilcdc", ("milan", "descmem_"): "pp", ("milan", "respmem_"): "pp",
    ("milan", "nvmmem_"): "pp", ("milan", "[BB:milan_datapath]"): None,   # first-party datapath
    ("milan_mac", "phy"): "eth", ("milan_mac", "core"): "eth", ("milan_mac", "tx_sf"): "eth",
    ("milan_mac", "mac_tx_cdc"): "eth", ("milan_mac", "mac_rx_cdc"): "eth",
    ("milan_mac", "[BB:KL_gptp_gmii_launch]"): "macfp", ("milan_mac", "[BB:KL_mac_rmon_events]"): "macfp",
    ("milan_mac", "[BB:ICAPE2]"): "macfp",
}
CSR_RULES = [
    (r"^ctrl", "ctrl"), (r"^ddrphy", "ddr"), (r"^sdram", "ddr"), (r"^identifier_mem", "ident"),
    (r"^milan_mac_phy_mdio", "mdio"), (r"^milan_mac_phy_crg", "eth"), (r"^milan_mac_core", "eth"),
    (r"^milan_mac_loopback$", "loop"), (r"^milan_mac_link_status$", "link"), (r"^milan_mac$", "eth"),
    (r"^spiflash", "spi"), (r"^timer0", "timer"), (r"^uart", "uart"), (r"^ppmem", "pp"),
]
CPU_PLACED = {
    "(VexiiRiscvLitex_": "cpu", "vexiis_0_logic_core": "cpu", "unified_mBus_arbiter_core": "cpu",
    "peripheral_bus_decoder_core": "cpu",
    "dma_bridge_read_bridge": "pp", "dma_bridge_write_bridge": "pp",
    "dma_filter_down_to_unified_mBus_cc": "pp",
    "ioBus_to_peripheral_bus_cc": "bus", "peripheral_toAxiLite4_logic_bridge": "bus",
    "mem_toAxi4_logic_bridge": "ddr", "unified_mBus_to_mem_toAxi4_up_widthAdapter": "ddr",
    "peripheral_clint_thread_core": "irq", "peripheral_clint_time_cc_driver": "irq",
    "peripheral_plic_intc_thread_logic": "irq",
}
SPLIT = [  # (object, regex proving milan_soc.py builds it, row)
    ("CtrlMemory wishbone.SRAM banks", r"bank = wishbone\.SRAM\(", "ctrlmem"),
    ("CtrlMemory wishbone.Decoder", r"self\.decoder = wishbone\.Decoder\(", "ctrlmem"),
    ("CtrlMemory error answer past the last bank", r"hole\.err\.eq\(", "ctrlmem"),
    ("CtrlMailbox EventManager", r"self\.ev = EventManager\(\)", "ctrlmbx"),
    ("ctrl_mbx CSR bank", r"soc\.csr\.add\(\"ctrl_mbx\"", "ctrlmbx"),
    ("CtrlMailbox millisecond tick", r"ms_tick = Signal\(\)", "ctrlmbx"),
    ("ctrl_mbx bus slave window", r"soc\.bus\.add_slave\(\"ctrl_mbx\"", "bus"),
    ("ctrl_mbx interrupt line", r"soc\.irq\.add\(\"ctrl_mbx\"", "irq"),
    ("split drops BIOS ROM and SRAM", r"integrated_rom_size=0, integrated_sram_size=0", "bios_rom"),
]

fail = 0
row_hits = {}


def place(src, obj, key):
    global fail
    if key is None:
        print(f"{src} | {obj} | first-party, outside the census")
        return
    want = ROW[key]
    hits = [i for i, b in enumerate(blocks) if want in b]
    if len(hits) != 1:
        fail = 1
        print(f"{src} | {obj} | MISSING: row key {want!r} matches {len(hits)} rows")
        return
    row_hits.setdefault(key, 0)
    row_hits[key] += 1
    stage, fate = (c.strip() for c in rows[hits[0]].split("|")[3:5])
    if not stage or not fate:
        fail = 1
        print(f"{src} | {obj} | MISSING stage or fate in row {want!r}")
        return
    print(f"{src} | {obj} | {want} | stage {stage}")


# 1. litex.log tree
cur = None
for line in tree_path.read_text(encoding="utf-8").splitlines()[1:]:
    m = re.match(r"^((?:│    |     )*)(?:├── |└── )(.*)$", line)
    if not m:
        continue
    depth, name = len(m.group(1)) // 5, m.group(2)
    if depth == 0:
        cur = name.split()[0]
        if cur not in RULES_TREE0:
            fail = 1
            print(f"tree | {cur} | MISSING: no rule")
            continue
        place("tree", name, RULES_TREE0[cur])
    elif depth == 1 and cur in ("cpu", "crg", "milan", "milan_mac"):
        key = next((v for (p, k), v in RULES_TREE1.items() if p == cur and name.startswith(k)), "?")
        if key == "?":
            fail = 1
            print(f"tree | {cur}.{name} | MISSING: no rule")
            continue
        place("tree", f"{cur}.{name}", key)

# 2. csr.csv
for line in csr_path.read_text(encoding="utf-8").splitlines():
    f = line.split(",")
    if f[0] not in ("csr_register", "csr_base"):
        continue
    key = next((v for rx, v in CSR_RULES if re.search(rx, f[1])), None)
    if key is None:
        fail = 1
        print(f"csr | {f[1]} | MISSING: no rule")
        continue
    place(f"csr {f[0]}", f[1], key)

# 3. CPU wrapper placed children
rpt = rpt_path.read_text(encoding="utf-8").splitlines()
start = next(i for i, s in enumerate(rpt) if re.match(r"^\|   VexiiRiscvLitex_", s))
for s in rpt[start + 1:]:
    if re.match(r"^\|   \S", s):
        break
    m = re.match(r"^\|     (\S+)\s+\|\s+\S+\s+\|\s+(\d+)", s)
    if not m:
        continue
    name = m.group(1)
    key = next((v for k, v in CPU_PLACED.items() if name.startswith(k)), None)
    if key is None:
        fail = 1
        print(f"placed | {name} | MISSING: no rule")
        continue
    place("placed", f"{name} {m.group(2)} LUT", key)

# 4. split-only LiteX parts at the head
for obj, rx, key in SPLIT:
    if not re.search(rx, soc):
        fail = 1
        print(f"split | {obj} | NOT BUILT at this head (regex {rx!r})")
        continue
    place("split", obj, key)

unused = [ROW[k] for k in ROW if k not in row_hits and k != "led"]
print(f"census rows: {len(rows)}; rows no object maps to: {unused or 'none'} (LEDs or GPIO: none built)")
print("RESULT:", "FAIL" if fail else "PASS")
sys.exit(fail)
