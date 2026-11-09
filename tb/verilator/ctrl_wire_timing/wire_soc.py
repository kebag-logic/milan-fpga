# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The wire-timing harness's CPU half (#665, #868): the CPU budget harness's split SoC, its mailbox host port on pads.

The CPU, its firmware memory and the flash are the CPU budget harness's
(tb/verilator/ctrl_service_budget/split_soc.py, imported read only), and so
are the CSR window's and the UART's pads, which the split boot simulation adds
(tb/verilator/ctrl_split_boot/boot_soc.py, imported read only):

  - the shipping VexiiRiscv with the split placement's instruction cache, at
    the 100 MHz product clock (the shape's sys clock, by the owner's decision
    of 2026-10-30 on #665) on this base's own CPU clock input, so its crossing
    to the bus is at equal frequencies, as the hook harness's `sys` clock;
  - milan_soc.add_ctrl_memory built from the linked platform image;
  - LiteSPI and timer0 where F1's port addresses them, the flash device the
    testbench's native model;
  - the Milan CSR window and the UART, their buses on pads.

One part differs: the mailbox. The CPU budget harness builds KL_mbx inside the
SoC, its datapath side on the testbench's pads. Here the SoC holds only
KL_mbx_wb, CtrlMailbox's Wishbone adapter, and its host port is on pads. The
testbench hands every access to the split placement's own top
(tb/verilator/milan_dp/tb_split_top.sv), whose KL_mbx reaches the
CTRL_SPLIT_P = 1 datapath through KL_mbx_cdc. So the mailbox, its crossing
and the datapath are the split top's, built by milan_dp's split recipe, and
the CPU reaches them only through KL_mbx_wb's host port and the CSR window.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_split_boot'))
import boot_soc  # noqa: E402  the split boot simulation's SoC, read only
import split_soc  # noqa: E402  the CPU budget harness's SoC, read only
from migen import ClockSignal, Instance, ResetSignal, Signal  # noqa: E402
from litex.build.generic_platform import Pins, Subsignal  # noqa: E402
from litex.build.sim.config import SimConfig  # noqa: E402
from litex.gen import LiteXModule  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402
from litex.soc.integration.builder import Builder  # noqa: E402
from litex.soc.integration.soc import SoCRegion  # noqa: E402
from litex.soc.interconnect import wishbone  # noqa: E402
from unittest.mock import patch  # noqa: E402

milan_soc = split_soc.milan_soc
capture_soc = split_soc.capture_soc


def host_pads(addr_w: int) -> list:
    """KL_mbx_wb's host port on the testbench's pads: the request, and the answer the split top gives."""
    fields = (('req', 1), ('we', 1), ('addr', addr_w), ('wdata', 32), ('be', 4), ('ack', 1), ('rdata', 32))
    return [('mbx_host', 0, *[Subsignal(n, Pins(w)) for n, w in fields])]


class HostPortMailbox(LiteXModule):
    """CtrlMailbox's KL_mbx_wb with no KL_mbx behind it: the host port is on pads, answered by the split top.

    Its constructor takes split_soc.StimulusMailbox's arguments, so split_soc.add_devices places it where the
    image addresses the mailbox; the datapath-side pads that harness drives are left unused."""

    pads = None   # the mbx_host resource, set by build() before add_devices runs

    def __init__(self, _unused_pads: object, _sys_clk_freq: int, _contract: object, _n_if: int) -> None:
        pads = HostPortMailbox.pads
        self.bus = wishbone.Interface(data_width=32, adr_width=30)
        self.specials += Instance('KL_mbx_wb',
            i_clk_i=ClockSignal('sys'), i_rst_n=~ResetSignal('sys'),
            i_wb_cyc_i=self.bus.cyc, i_wb_stb_i=self.bus.stb, i_wb_we_i=self.bus.we,
            i_wb_adr_i=self.bus.adr, i_wb_dat_i=self.bus.dat_w, i_wb_sel_i=self.bus.sel,
            o_wb_ack_o=self.bus.ack, o_wb_dat_o=self.bus.dat_r, o_wb_err_o=self.bus.err,
            o_host_req_o=pads.req, o_host_we_o=pads.we, o_host_addr_o=pads.addr, o_host_wdata_o=pads.wdata,
            o_host_be_o=pads.be, i_host_ack_i=pads.ack, i_host_rdata_i=pads.rdata)


def build(build_dir: Path, shape: str, elf: Path, n_if: int, flash_map: Path) -> dict:
    """Export the CPU half's Verilog and csr.csv; return the native build's inputs."""
    if n_if != 1:
        raise RuntimeError(f'the split top connects one interface (tb_split_top.sv, CtrlMailbox._split); '
                           f'{n_if} asked')
    addresses = split_soc.fixture_addresses(flash_map)
    cfg = capture_soc.eb.load_config(str(ROOT / 'configs' / (shape + '.yaml')))
    clocks, params = cfg['constraints'], cfg['soc']
    contract = milan_soc.ctrl_mailbox_contract()
    platform = split_soc.platform_for(contract, n_if)
    addr_w = split_soc.widths(contract, n_if)['addr']
    platform.add_extension([('milan_csr', 0, *[Subsignal(n, Pins(w)) for n, w in boot_soc.CSR_FIELDS])])
    platform.add_extension(host_pads(addr_w))
    HostPortMailbox.pads = platform.request('mbx_host')
    cpu = split_soc.CpuPatches('cover')
    geometry = split_soc.fetch_l1_geometry('split')
    scala_args = [*params['scala_args'], *filter(None, [milan_soc.ctrl_cpu_args(geometry)])]
    sys_hz = clocks['sys_clk_hz']
    cpu_hz = sys_hz   # the product's split CPU clock (see the module's docstring)
    with cpu.applied(), patch.object(split_soc, 'StimulusMailbox', HostPortMailbox):
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
        soc.milan_csr = boot_soc.CsrWindow(platform.request('milan_csr'))
        soc.bus.add_slave('milan_csr', soc.milan_csr.bus, region=SoCRegion(
            origin=milan_soc.MILAN_CSR_BASE, size=milan_soc.MILAN_CSR_SIZE, cached=False))
        builder = Builder(soc, output_dir=str(build_dir), compile_software=False, compile_gateware=False,
                          csr_csv=str(build_dir / 'csr.csv'))
        sim_config = SimConfig()
        sim_config.add_clocker('sys_clk', freq_hz=sys_hz)
        sim_config.add_clocker('milan_clk', freq_hz=cpu_hz)
        builder.build(run=False, sim_config=sim_config)
    boot_soc.refuse_deviation(build_dir / 'csr.csv', flash_map)
    spec = {
        'sources': [str(Path(s[0]).resolve()) for s in soc.platform.sources],
        'includes': soc.platform.verilog_include_paths,
        'sys_hz': sys_hz, 'cpu_hz': cpu_hz, 'shape': shape, 'interfaces': n_if,
        'addresses': addresses, 'csr_base': milan_soc.MILAN_CSR_BASE, 'csr_size': milan_soc.MILAN_CSR_SIZE,
        'host_addr_bits': addr_w, 'window_bytes': contract.window_bytes,
        'netlist': VexiiRiscv.netlist_name, 'memory_regions': cpu.soc_regions,
        'cpu_memory_regions': [list(r) for r in VexiiRiscv.memory_regions],
        'fetch_l1_geometry': list(geometry) if geometry else None,
        'ctrl_plan': soc.ctrl_plan.summary(),
    }
    (build_dir / 'soc.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec


if __name__ == '__main__':
    print(json.dumps(build(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), int(sys.argv[4]),
                           Path(sys.argv[5]))))
