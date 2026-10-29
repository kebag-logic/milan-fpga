# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split boot simulation's SoC (#665): the CPU budget harness's test-only split SoC, with the CSR window
and UART on pads.

The CPU, its firmware memory, the mailbox and the flash are the CPU budget
harness's (tb/verilator/ctrl_service_budget/split_soc.py, imported read only):
the shipping VexiiRiscv with the split placement's instruction cache at the
Milan clock, milan_soc.add_ctrl_memory built from the linked image, KL_mbx
behind KL_mbx_wb with its datapath on the testbench's pads and the face
commit acknowledged at the contract's bound, LiteSPI and timer0 where F1's
port addresses them. That harness's SoC has neither of the two devices the
platform adds, so this one adds them:

  - the Milan CSR window, a Wishbone slave at milan_soc.MILAN_CSR_BASE named
    milan_csr as the product SoC names it, its bus on pads: the testbench
    answers it from a register file and logs every access with its cycle;
  - the UART, MilanSoC's own `sim` UART, whose stream the testbench reads and
    writes.

The datapath is not built: the window answers as the datapath's reset
registers do where the boot reads them (ID, VERSION) and from gate 35's seeded
file elsewhere, so the boot's write trace compares with milan_baremetal.c's on
the same file. The image addresses every device through ctrl_plat_gen.py's
map, from this SoC's own csr.csv.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import split_soc  # noqa: E402  the CPU budget harness's SoC, read only
from litex.build.generic_platform import Pins, Subsignal  # noqa: E402
from litex.build.sim.config import SimConfig  # noqa: E402
from litex.gen import LiteXModule  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402
from litex.soc.integration.builder import Builder  # noqa: E402
from litex.soc.integration.soc import SoCRegion  # noqa: E402
from litex.soc.interconnect import wishbone  # noqa: E402

milan_soc = split_soc.milan_soc
capture_soc = split_soc.capture_soc
#: The window's Wishbone signals on the testbench's pads.
CSR_FIELDS = (('cyc', 1), ('stb', 1), ('we', 1), ('adr', 30), ('dat_w', 32), ('sel', 4), ('dat_r', 32), ('ack', 1))


class CsrWindow(LiteXModule):
    """The Milan CSR window's bus, answered by the testbench."""

    def __init__(self, pads: object) -> None:
        self.bus = wishbone.Interface(data_width=32, adr_width=30)
        self.comb += [pads.cyc.eq(self.bus.cyc), pads.stb.eq(self.bus.stb), pads.we.eq(self.bus.we),
                      pads.adr.eq(self.bus.adr), pads.dat_w.eq(self.bus.dat_w), pads.sel.eq(self.bus.sel),
                      self.bus.dat_r.eq(pads.dat_r), self.bus.ack.eq(pads.ack)]


def build(build_dir: Path, shape: str, elf: Path, n_if: int) -> dict:
    """Export the boot SoC's Verilog and csr.csv; return the native build's inputs."""
    addresses = split_soc.fixture_addresses()
    cfg = capture_soc.eb.load_config(str(ROOT / 'configs' / (shape + '.yaml')))
    clocks, params = cfg['constraints'], cfg['soc']
    contract = milan_soc.ctrl_mailbox_contract()
    deviations = split_soc.ack_deviations(contract)
    if deviations:
        raise RuntimeError(f'the commit acknowledgement is not at the contract bound: {deviations}')
    platform = split_soc.platform_for(contract, n_if)
    platform.add_extension([('milan_csr', 0, *[Subsignal(n, Pins(w)) for n, w in CSR_FIELDS])])
    cpu = split_soc.CpuPatches('cover')
    geometry = split_soc.fetch_l1_geometry('split')
    scala_args = [*params['scala_args'], *filter(None, [milan_soc.ctrl_cpu_args(geometry)])]
    sys_hz, cpu_hz = clocks['sys_clk_hz'], clocks['milan_clk_hz']
    with cpu.applied():
        soc = milan_soc.MilanSoC(
            platform, sys_hz, xlen=params['xlen'], cpu_count=params['cpu_count'], cpu=params['cpu'],
            board='ax7101', with_milan=False, with_mac=False, with_dram=False, with_spiflash=False,
            flashboot=clocks['flashboot'], milan_clk_freq=cpu_hz, l2_bytes=clocks['l2_bytes'],
            extra_scala_args=scala_args, uart_name='sim', uart_baudrate=clocks['uart_baudrate'],
            integrated_rom_size=0, integrated_sram_size=0, integrated_main_ram_size=0, with_timer=False)
        milan_soc.add_ctrl_memory(soc, elf)
        for path in split_soc.mailbox_sources(n_if, build_dir / 'mbx-variant'):
            platform.add_source(str(path))
        split_soc.add_devices(soc, platform, addresses, contract, n_if)
        soc.milan_csr = CsrWindow(platform.request('milan_csr'))
        soc.bus.add_slave('milan_csr', soc.milan_csr.bus, region=SoCRegion(
            origin=milan_soc.MILAN_CSR_BASE, size=milan_soc.MILAN_CSR_SIZE, cached=False))
        builder = Builder(soc, output_dir=str(build_dir), compile_software=False, compile_gateware=False,
                          csr_csv=str(build_dir / 'csr.csv'))
        sim_config = SimConfig()
        sim_config.add_clocker('sys_clk', freq_hz=sys_hz)
        sim_config.add_clocker('milan_clk', freq_hz=cpu_hz)
        builder.build(run=False, sim_config=sim_config)
    spec = {
        'sources': [str(Path(s[0]).resolve()) for s in soc.platform.sources],
        'includes': soc.platform.verilog_include_paths,
        'sys_hz': sys_hz, 'cpu_hz': cpu_hz, 'shape': shape, 'interfaces': n_if,
        'addresses': addresses, 'csr_base': milan_soc.MILAN_CSR_BASE, 'csr_size': milan_soc.MILAN_CSR_SIZE,
        'netlist': VexiiRiscv.netlist_name, 'memory_regions': cpu.soc_regions,
        'cpu_memory_regions': [list(r) for r in VexiiRiscv.memory_regions],
        'ctrl_plan': soc.ctrl_plan.summary(),
    }
    (build_dir / 'soc.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec
