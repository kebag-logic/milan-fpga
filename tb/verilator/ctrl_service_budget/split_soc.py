# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The test-only split SoC: the shipping CPU, the image's block RAM and a driven mailbox.

The CPU is built by MilanSoC's own VexiiRiscv path: cacheless RV32I, one hart,
the CPU at the 50 MHz Milan clock and the bus at 100 MHz, with the DMA port
the shipping image has. Its firmware memory is milan_soc.add_ctrl_memory,
the split placement's, built from the linked image. The capture harness's
product simulation (tb/verilator/nvm_capture_cpu/soc.py) is imported read
only, for its simulated clocks and its path to the product sources.

The image ctrl_srp_image.py links is a size fixture whose bus addresses are
placeholders (#665): the mailbox at ctrl_build.py's CTRL_MBX_BASE and the
LiteSPI master, timer0 and flash window of ctrl_nvm/test/rv32/generated.
This SoC puts each device where the unmodified image addresses it, and reads
those addresses from the fixture's own sources, never restating them. The
mailbox is this harness's own instance of KL_mbx behind KL_mbx_wb, the
CtrlMailbox hookup with the receive and transmit streams, the link levels
and the grandmaster on pads the testbench drives. Every other KL_mbx port is
connected as CtrlMailbox connects it: the publication block's outputs (contract
2.2) named and unread, and the face block's (contract 2.3) by
milan_soc.ctrl_mailbox_face_ports, at the build's interface count, its outputs
named and unread and its inputs held idle by name. The flash keeps
LiteSPI's crossbar, memory-mapped reader and command master, with the master
in its own CSR bank, and the serial device is the sibling service-budget
harness's native model (fw_service_budget/flash.hpp).
"""
from __future__ import annotations

import contextlib
import json
import re
import sys
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CAPTURE = ROOT / 'tb/verilator/nvm_capture_cpu'
FIXTURE_GEN = ROOT / 'sw/firmware/ctrl_nvm/test/rv32/generated'
CSR_BANK_BYTES = 0x800
sys.path.insert(0, str(CAPTURE))
import soc as capture_soc  # noqa: E402  the capture harness's simulation, read only
from migen import ClockSignal, If, Instance, ResetSignal, Signal  # noqa: E402
from litex.build.generic_platform import Pins, Subsignal  # noqa: E402
from litex.build.sim.config import SimConfig  # noqa: E402
from litex.gen import LiteXModule  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402
from litex.soc.integration.builder import Builder  # noqa: E402
from litex.soc.integration.soc import SoCRegion  # noqa: E402
from litex.soc.interconnect import stream, wishbone  # noqa: E402
from litex.tools.litex_sim import Platform  # noqa: E402
from litespi import LiteSPI  # noqa: E402
from litespi.common import spi_core2phy_layout, spi_phy2core_layout  # noqa: E402
from litespi.core.master import LiteSPIMaster  # noqa: E402
from litespi.modules import N25Q128A13  # noqa: E402
from litespi.opcodes import SpiNorFlashOpCodes as SpiCodes  # noqa: E402

milan_soc = capture_soc.milan_soc
#: The fixture's register offsets, in the order its csr.h writes them.
MASTER_LAYOUT = ([0x0, 0x4, 0x8], ['0xc'])
TIMER_LAYOUT = [('load', '0x0'), ('reload', '0x4'), ('en', '0x8'), ('update_value', '0xc'), ('value', '0x10')]


def fixture_addresses() -> dict[str, int]:
    """The placeholder addresses the unmodified image is compiled against."""
    sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl/test'))
    sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
    import ctrl_build
    found = {}
    for flag in ctrl_build.RV32_FLAGS:
        match = re.fullmatch(r'-DCTRL_MBX_BASE=(0x[0-9a-fA-F]+)u?', flag)
        if match:
            found['mailbox'] = int(match.group(1), 16)
    csr_h = (FIXTURE_GEN / 'csr.h').read_text()
    mem_h = (FIXTURE_GEN / 'mem.h').read_text()
    for key, text, name in (('master', csr_h, 'CSR_SPIFLASH_MASTER_BASE'),
                            ('timer0', csr_h, 'CSR_TIMER0_BASE'),
                            ('flash', mem_h, 'SPIFLASH_BASE'),
                            ('flash_size', mem_h, 'SPIFLASH_SIZE')):
        values = re.findall(rf'#define {name}\s+(0x[0-9a-fA-F]+)u', text)
        if len(values) != 1:
            raise RuntimeError(f'fixture address {name} is not defined exactly once')
        found[key] = int(values[0], 16)
    # The master's four registers in the fixture's order, one 32-bit word each.
    base = r'CSR_SPIFLASH_MASTER_BASE \+ (0x[0-9a-f]+)u'
    offsets = [int(v, 16) for v in re.findall(
        r'spiflash_master_(?:cs|phyconfig|rxtx)_write\(uint32_t v\) \{ csr_wr\(' + base, csr_h)]
    status = re.findall(r'spiflash_master_status_read\(void\) \{ return csr_rd\(' + base, csr_h)
    if (offsets, status) != MASTER_LAYOUT:
        raise RuntimeError('fixture LiteSPI master layout is not cs, phyconfig, rxtx, status')
    timer = re.findall(r'timer0_(\w+)_(?:write|read)\((?:uint32_t v|void)\) \{ (?:return )?'
                       r'csr_(?:wr|rd)\(CSR_TIMER0_BASE \+ (0x[0-9a-f]+)u', csr_h)
    if timer != TIMER_LAYOUT:
        raise RuntimeError('fixture timer0 layout is not load, reload, en, update_value, value')
    if set(found) != {'mailbox', 'master', 'timer0', 'flash', 'flash_size'}:
        raise RuntimeError(f'fixture addresses incomplete: {sorted(found)}')
    return found


def mailbox_sources(n_if: int, gen_dir: Path) -> list[Path]:
    """The shipping mailbox RTL; at two interfaces, its generator's variant package and top."""
    sources = [ROOT / name for name in milan_soc._CTRL_MAILBOX_SOURCES]
    if n_if == 1:
        return sources
    sys.path.insert(0, str(ROOT / 'sw/mailbox'))
    import gen_mailbox
    findings = gen_mailbox.write_variant(gen_mailbox.load(), n_if, gen_dir)
    if findings:
        raise RuntimeError(f'mailbox variant findings: {findings}')
    variant = {'KL_mbx_pkg.sv': gen_dir / 'KL_mbx_pkg.sv', 'KL_mbx.sv': gen_dir / 'KL_mbx.sv'}
    return [variant.get(path.name, path) for path in sources]


def power_of_two_cover(regions: list[tuple]) -> list[tuple]:
    """Each region at its power-of-two size, refused where a cover would reach another region.

    The CPU generator decodes a region whose size is not a power of two
    wrongly: for rom, 224 KiB at 0, it emits (address & 0xfffc8000) == 0,
    which leaves out every address with bit 15 set, so the first fetch at
    0x8000 or above takes an instruction access fault (cause 1). The cover
    changes only the generator's address decode (its region checks and its
    bus decoder), never a register or a pipeline stage; the SoC's own bus
    regions and CtrlMemory's banks, whose decode answers err past the last
    bank, stay as shipped.
    """
    covered = []
    for origin, size, mode, bus in regions:
        cover = 1 << (size - 1).bit_length()
        if origin % cover:
            raise RuntimeError(f'region at 0x{origin:08x} is not aligned to its cover')
        for other in regions:
            if other[0] != origin and origin <= other[0] < origin + cover:
                raise RuntimeError(f'the cover of 0x{origin:08x} reaches 0x{other[0]:08x}')
        covered.append((origin, cover, mode, bus))
    return covered


def widths(contract: object, n_if: int) -> dict[str, int]:
    """The host address, interface and channel widths KL_mbx_pkg derives."""
    return dict(addr=(contract.window_bytes // 4 - 1).bit_length(), interface=max(1, (n_if - 1).bit_length()),
                channel=max(1, (len(contract.channels) - 1).bit_length()))


def platform_for(contract: object, n_if: int) -> object:
    """The simulation platform: the clocks, the mailbox's datapath pads and the flash device's."""
    w = widths(contract, n_if)
    platform = Platform()
    platform.add_extension([('milan_clk', 0, Pins(1)), ('audio_clk', 0, Pins(1)),
                            ('audio_tdm_clk', 0, Pins(1)), ('sys_reset', 0, Pins(1))])
    mbx_fields = [('link_up', n_if), ('gm_change', n_if), ('gm_id', 64 * n_if), ('domain', 8 * n_if),
                  ('rx_valid', 1), ('rx_ready', 1), ('rx_data', 8), ('rx_last', 1), ('rx_if', w['interface']),
                  ('tx_valid', 1), ('tx_ready', 1), ('tx_data', 8), ('tx_last', 1), ('tx_if', w['interface']),
                  ('tx_ch', w['channel']), ('host_req', 1), ('host_we', 1), ('host_addr', w['addr']),
                  ('host_wdata', 32), ('host_ack', 1), ('host_rdata', 32), ('ms_tick', 1)]
    flash_fields = [('cs', 1), ('tx_valid', 1), ('tx_ready', 1), ('tx_data', 32), ('tx_len', 6),
                    ('tx_width', 4), ('rx_valid', 1), ('rx_ready', 1), ('rx_data', 32)]
    platform.add_extension([('mbx', 0, *[Subsignal(n, Pins(width)) for n, width in mbx_fields]),
                            ('flash', 0, *[Subsignal(n, Pins(width)) for n, width in flash_fields])])
    return platform


class StimulusMailbox(LiteXModule):
    """CtrlMailbox's hookup of KL_mbx_wb and KL_mbx, its datapath on the testbench's pads."""

    def __init__(self, pads: object, sys_clk_freq: int, contract: object, n_if: int) -> None:
        self.bus = wishbone.Interface(data_width=32, adr_width=30)
        # NOW_MS's one-cycle pulse per millisecond of the bus clock, as CtrlMailbox.
        ms_div = int(sys_clk_freq) // 1000
        ms_cnt = Signal(max=ms_div)
        ms_tick = Signal()
        self.sync += If(ms_cnt == ms_div - 1, ms_cnt.eq(0), ms_tick.eq(1)).Else(
            ms_cnt.eq(ms_cnt + 1), ms_tick.eq(0))
        req, we, ack = Signal(), Signal(), Signal()
        addr, wdata, rdata, be = Signal(widths(contract, n_if)['addr']), Signal(32), Signal(32), Signal(4)
        self.comb += [pads.host_req.eq(req), pads.host_we.eq(we), pads.host_addr.eq(addr),
                      pads.host_wdata.eq(wdata), pads.host_ack.eq(ack), pads.host_rdata.eq(rdata),
                      pads.ms_tick.eq(ms_tick)]
        self.specials += Instance('KL_mbx_wb',
            i_clk_i=ClockSignal('sys'), i_rst_n=~ResetSignal('sys'),
            i_wb_cyc_i=self.bus.cyc, i_wb_stb_i=self.bus.stb, i_wb_we_i=self.bus.we,
            i_wb_adr_i=self.bus.adr, i_wb_dat_i=self.bus.dat_w, i_wb_sel_i=self.bus.sel,
            o_wb_ack_o=self.bus.ack, o_wb_dat_o=self.bus.dat_r, o_wb_err_o=self.bus.err,
            o_host_req_o=req, o_host_we_o=we, o_host_addr_o=addr, o_host_wdata_o=wdata,
            o_host_be_o=be, i_host_ack_i=ack, i_host_rdata_i=rdata)
        self.specials += Instance('KL_mbx',
            i_clk_i=ClockSignal('sys'), i_rst_n=~ResetSignal('sys'),
            i_host_req_i=req, i_host_we_i=we, i_host_addr_i=addr, i_host_wdata_i=wdata,
            i_host_be_i=be, o_host_ack_o=ack, o_host_rdata_o=rdata, o_irq_o=Signal(),
            i_ms_tick_p_i=ms_tick,
            i_link_up_i=pads.link_up, i_gm_change_p_i=pads.gm_change, i_gm_id_i=pads.gm_id,
            i_gptp_domain_i=pads.domain,
            i_rx_valid_i=pads.rx_valid, o_rx_ready_o=pads.rx_ready, i_rx_data_i=pads.rx_data,
            i_rx_last_i=pads.rx_last, i_rx_if_i=pads.rx_if,
            o_tx_valid_o=pads.tx_valid, i_tx_ready_i=pads.tx_ready, o_tx_data_o=pads.tx_data,
            o_tx_last_o=pads.tx_last, o_tx_if_o=pads.tx_if, o_tx_ch_o=pads.tx_ch,
            **unread_publication(contract, n_if), **face_ports(contract, n_if))


def unread_publication(contract: object, n_if: int) -> dict[str, object]:
    """The publication block's outputs (contract 2.2), named and left unread as CtrlMailbox leaves them."""
    pub_w = {(r.name, f.name): f.width for r in contract.pub_registers for f in r.fields}
    return dict(o_pub_da_gate_o=Signal(n_if * contract.pub_sources),
                o_pub_licence_o=Signal(n_if * contract.pub_sources),
                o_pub_idle_slope_bps_o=Signal(n_if * pub_w[('IDLE_SLOPE', 'BPS')]),
                o_pub_dom_vid_o=Signal(n_if * pub_w[('SR_DOMAIN', 'VID')]),
                o_pub_dom_prio_o=Signal(n_if * pub_w[('SR_DOMAIN', 'PRIORITY')]),
                o_pub_dom_adopted_o=Signal(n_if * pub_w[('SR_DOMAIN', 'ADOPTED')]),
                o_pub_talker_decl_o=Signal(n_if * contract.pub_sources),
                o_pub_bound_o=Signal(n_if * contract.pub_sinks),
                o_pub_sid_valid_o=Signal(n_if * contract.pub_sinks),
                o_pub_started_o=Signal(n_if * contract.pub_sinks),
                o_pub_sid_o=Signal(n_if * contract.pub_sinks * 64))


#: The face block's inputs (contract 2.3), each held idle by name as CtrlMailbox holds it: the
#: datapath's commit acknowledgement, the four windows' answers and the face events.
FACE_IDLE_INPUTS = dict(
    i_fw_ack_p_i=0,
    i_ctr_ans_p_i=0, i_ctr_ans_tag_i=0, i_ctr_ans_data_i=0,
    i_amap_ans_p_i=0, i_amap_ans_tag_i=0, i_amap_ans_data_i=0,
    i_edit_ans_p_i=0, i_edit_ans_tag_i=0, i_edit_ans_data_i=0,
    i_gsi_ans_p_i=0, i_gsi_ans_tag_i=0, i_gsi_ans_data_i=0,
    i_ctr_chg_p_i=0, i_ctr_chg_type_i=0, i_ctr_chg_index_i=0, i_avb_chg_p_i=0, i_asp_chg_p_i=0, i_amap_wr_p_i=0)


def face_ports(contract: object, n_if: int) -> dict[str, object]:
    """The face block's ports (contract 2.3) as CtrlMailbox connects them, at n_if interfaces:
    every output a named Signal of its generated width, left unread (ctrl_mailbox_face_ports),
    and every input held idle by name, refused unless exactly the inputs CtrlMailbox holds idle."""
    from mailbox_model import with_interfaces
    ports = milan_soc.ctrl_mailbox_face_ports(with_interfaces(contract, n_if))
    held = {name: value for name, value in ports.items() if name.startswith('i_')}
    if held != FACE_IDLE_INPUTS:
        raise RuntimeError('the face inputs differ from those CtrlMailbox holds idle: '
                           f'{sorted(set(held.items()) ^ set(FACE_IDLE_INPUTS.items()))}')
    return {**ports, **FACE_IDLE_INPUTS}


class FlashBoundary(LiteXModule):
    """The LiteSPI PHY's endpoint on pads; the native model is the serial device."""

    def __init__(self, pads: object, module: object) -> None:
        self.flash = module
        self.sink = stream.Endpoint(spi_core2phy_layout)
        self.source = stream.Endpoint(spi_phy2core_layout)
        self.cs = Signal()
        self.dummy_bits = Signal(8)
        self.comb += [pads.cs.eq(self.cs), pads.tx_valid.eq(self.sink.valid),
                      self.sink.ready.eq(pads.tx_ready), pads.tx_data.eq(self.sink.data),
                      pads.tx_len.eq(self.sink.len), pads.tx_width.eq(self.sink.width),
                      self.source.valid.eq(pads.rx_valid), pads.rx_ready.eq(self.source.ready),
                      self.source.data.eq(pads.rx_data)]


def add_devices(soc: object, platform: object, addresses: dict[str, int], contract: object, n_if: int) -> None:
    """The mailbox, the flash and timer0, each where the fixture addresses it."""
    soc.ctrl_mbx = StimulusMailbox(platform.request('mbx'), soc.sys_clk_freq, contract, n_if)
    soc.bus.add_slave('ctrl_mbx', soc.ctrl_mbx.bus, region=SoCRegion(
        origin=addresses['mailbox'], size=contract.window_bytes, cached=False))
    module = N25Q128A13(SpiCodes.READ_1_1_1_FAST)
    if module.total_size != addresses['flash_size']:
        raise RuntimeError('fixture flash window size differs from the shipping part')
    phy = FlashBoundary(platform.request('flash'), module)
    spiflash = LiteSPI(phy, mmap_endianness=soc.cpu.endianness, with_master=False)
    spiflash.add_module(name='phy', module=phy)
    master = LiteSPIMaster(tx_fifo_depth=1, rx_fifo_depth=1, cs_width=len(phy.cs))
    port = spiflash.crossbar.get_port(master.cs)
    spiflash.comb += [port.source.connect(master.sink), master.source.connect(port.sink)]
    soc.add_module(name='spiflash', module=spiflash)
    soc.bus.add_slave(name='spiflash', slave=spiflash.bus, strip_origin=True, region=SoCRegion(
        origin=addresses['flash'], size=module.total_size, mode=spiflash.bus.mode + 'x'))
    csr_base = soc.mem_map['csr']
    for name in ('master', 'timer0'):
        if (addresses[name] - csr_base) % CSR_BANK_BYTES:
            raise RuntimeError(f'fixture {name} is not at a CSR bank boundary')
    soc.csr.add('spiflash_master', n=(addresses['master'] - csr_base) // CSR_BANK_BYTES)
    soc.add_module(name='spiflash_master', module=master)
    soc.csr.add('timer0', n=(addresses['timer0'] - csr_base) // CSR_BANK_BYTES)
    soc.add_timer('timer0')


class CpuPatches:
    """MilanSoC's VexiiRiscv path as shipped, with the DMA port and the selected region set."""

    def __init__(self, cpu_regions: str) -> None:
        if cpu_regions not in ('cover', 'as-built'):
            raise RuntimeError(f'unknown cpu_regions {cpu_regions}')
        self.cpu_regions = cpu_regions
        self.soc_regions: list[list] = []
        self.args_read = VexiiRiscv.args_read
        self.netlist_name = VexiiRiscv.generate_netlist_name

    def shipping_args_read(self, args: object) -> None:
        """The shipping image's CPU has the DMA port (with_dma = with_milan); keep it, idle."""
        args.with_dma = True
        self.args_read(args)

    def generate_netlist_name(self) -> None:
        """Hand the generator the regions cpu_regions selects; record the SoC's own."""
        self.soc_regions[:] = [list(r) for r in VexiiRiscv.memory_regions]
        if self.cpu_regions == 'cover':
            VexiiRiscv.memory_regions = power_of_two_cover(VexiiRiscv.memory_regions)
        self.netlist_name()

    def applied(self) -> contextlib.ExitStack:
        """The patches, as one context."""
        stack = contextlib.ExitStack()
        stack.enter_context(patch.object(milan_soc, '_CRG', capture_soc.SimClocks))
        stack.enter_context(patch.object(VexiiRiscv, 'args_read', staticmethod(self.shipping_args_read)))
        stack.enter_context(patch.object(VexiiRiscv, 'generate_netlist_name',
                                         staticmethod(self.generate_netlist_name)))
        return stack


def ledgered_plan(name: str | None) -> contextlib.AbstractContextManager:
    """add_ctrl_memory's plan held to the named ledgered point's tiles (ctrl_memory.LEDGERED), which
    refuses any image that is not that point; None keeps the SoC build's plan, which names none."""
    if name is None:
        return contextlib.nullcontext()
    plan = milan_soc.ctrl_memory.plan
    return patch.object(milan_soc.ctrl_memory, 'plan', lambda image, **kw: plan(image, ledgered=name, **kw))


def build(build_dir: Path, shape: str, elf: Path, n_if: int, cpu_regions: str = 'cover',
          ledgered: str | None = None) -> dict:
    """Export the test SoC's Verilog and return the native build's inputs.

    cpu_regions 'cover' gives the CPU generator each region at its
    power-of-two cover; 'as-built' gives it the SoC's regions unchanged,
    which reproduces the generator's rom decode defect (a control).
    ledgered names the ledgered point this build measures (build.ledgered_point),
    whose firmware memory is planned to that point's tiles.
    """
    addresses = fixture_addresses()
    cfg = capture_soc.eb.load_config(str(ROOT / 'configs' / (shape + '.yaml')))
    clocks, params = cfg['constraints'], cfg['soc']
    contract = milan_soc.ctrl_mailbox_contract()
    platform = platform_for(contract, n_if)
    cpu = CpuPatches(cpu_regions)
    sys_hz, cpu_hz = clocks['sys_clk_hz'], clocks['milan_clk_hz']
    with cpu.applied():
        soc = milan_soc.MilanSoC(
            platform, sys_hz, xlen=params['xlen'], cpu_count=params['cpu_count'], cpu=params['cpu'],
            board='ax7101', with_milan=False, with_mac=False, with_dram=False, with_spiflash=False,
            flashboot=clocks['flashboot'], milan_clk_freq=cpu_hz, l2_bytes=clocks['l2_bytes'],
            extra_scala_args=params['scala_args'], uart_name='sim', uart_baudrate=clocks['uart_baudrate'],
            integrated_rom_size=0, integrated_sram_size=0, integrated_main_ram_size=0, with_timer=False)
        with ledgered_plan(ledgered):
            milan_soc.add_ctrl_memory(soc, elf)
        for path in mailbox_sources(n_if, build_dir / 'mbx-variant'):
            platform.add_source(str(path))
        add_devices(soc, platform, addresses, contract, n_if)
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
        'addresses': addresses, 'window_bytes': contract.window_bytes,
        'netlist': VexiiRiscv.netlist_name,
        'vexii_soc_args': {k: str(v) for k, v in sorted(vars(VexiiRiscv.soc_args).items())},
        'vexii_args': VexiiRiscv.vexii_args,
        'memory_regions': cpu.soc_regions,
        'cpu_regions': cpu_regions,
        'cpu_memory_regions': [list(r) for r in VexiiRiscv.memory_regions],
        'ctrl_plan': soc.ctrl_plan.summary(),
    }
    (build_dir / 'soc.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec
