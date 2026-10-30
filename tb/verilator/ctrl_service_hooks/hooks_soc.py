# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The hook harness's test SoC (#665): the CPU budget harness's split SoC, with the platform's CSR window.

The CPU, its firmware memory, the mailbox and the flash are the CPU budget
harness's (tb/verilator/ctrl_service_budget/split_soc.py, imported read only):
the shipping VexiiRiscv with the split placement's instruction cache,
milan_soc.add_ctrl_memory built from the linked image, KL_mbx behind
KL_mbx_wb with its datapath on the testbench's pads and each face commit
acknowledged at the contract's bound, LiteSPI and timer0. The platform image
also reaches two devices that SoC lacks, so this one adds them:

  - the Milan CSR window at milan_soc.MILAN_CSR_BASE, answered here in
    gateware from a register file: ID and VERSION as the datapath's reset
    values, every other word the split boot simulation's seeded value until
    written, then the value written, and TOD_RD_LO/HI the simulated time of
    the last PTP_CMD snapshot (tb/verilator/ctrl_split_boot/sim_main.cpp
    answers the same words from the testbench);
  - the UART, MilanSoC's own `sim` UART, which the CPU budget harness's SoC
    already has.

The face block (contract 2.3) has two arms. `idle` connects it exactly as
the CPU budget harness does: its window answers and events held idle as
milan_soc.CtrlMailbox holds them. `answering` is a labelled test arm, a
datapath that answers the CTR and GSI windows at the slowest the contract
allows, wait_cycles - 1 cycles after the request opens, the last cycle
KL_mbx's window accepts, and whose counter-change event (ctr_chg_p_i) the
testbench drives (the `hook` pads): the H-COUNTERS push reads the CTR
window, so without an answer it is never sent. The AMAP and EDIT windows,
AVB_INFO, AS_PATH and live-map events stay idle in both arms.

The CPU runs at the shape's Milan clock, the product's split CPU clock, or at
a labelled test clock (cpu_hz); the bus stays at the shape's system clock.
"""
from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import split_soc  # noqa: E402  the CPU budget harness's SoC, read only
from migen import If, Memory, Signal  # noqa: E402
from litex.build.generic_platform import Pins, Subsignal  # noqa: E402
from litex.build.sim.config import SimConfig  # noqa: E402
from litex.gen import LiteXModule  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402
from litex.soc.integration.builder import Builder  # noqa: E402
from litex.soc.integration.soc import SoCRegion  # noqa: E402
from litex.soc.interconnect import wishbone  # noqa: E402

milan_soc = split_soc.milan_soc
capture_soc = split_soc.capture_soc
#: The face arms (see the module's docstring).
ARMS = ('idle', 'answering')
#: The windows the answering arm answers.
ANSWERED = ('CTR', 'GSI')
#: The CSR window's words the testbench of the split boot simulation answers (its Bench): ID 'MILN', VERSION
#: 0x0002_0060 (decision D2), and PTP_CMD's snapshot strobe (bit 2) with the two TOD_RD words it latches.
CSR_ID = (0x000, 0x4D494C4E)
CSR_VERSION = (0x004, 0x00020060)
PTP_CMD = 0x520
PTP_SNAPSHOT_BIT = 2
TOD_RD = (0x530, 0x534)


def seeded(offset: int) -> int:
    """A CSR word never written: the split boot simulation's seeded value (its Bench.word)."""
    return {CSR_ID[0]: CSR_ID[1], CSR_VERSION[0]: CSR_VERSION[1]}.get(offset, 0x5A000001 | (offset << 8))


class CsrFile(LiteXModule):
    """The Milan CSR window, a register file answering each access one cycle after it is presented."""

    def __init__(self, size: int, sys_hz: int) -> None:
        self.bus = wishbone.Interface(data_width=32, adr_width=30)
        words = size // 4
        bits = (words - 1).bit_length()
        mem = Memory(32, words, init=[seeded(4 * w) for w in range(words)])
        rd = mem.get_port()
        wr = mem.get_port(write_capable=True)
        self.specials += mem, rd, wr
        access = Signal()
        offset = Signal(bits)
        held = Signal(bits)
        now_ns = Signal(64)
        tod = Signal(64)
        self.comb += [access.eq(self.bus.cyc & self.bus.stb & ~self.bus.ack), offset.eq(self.bus.adr[:bits]),
                      rd.adr.eq(offset), wr.adr.eq(offset), wr.dat_w.eq(self.bus.dat_w),
                      wr.we.eq(access & self.bus.we)]
        self.sync += [now_ns.eq(now_ns + 1_000_000_000 // sys_hz), self.bus.ack.eq(access), held.eq(offset),
                      If(access & self.bus.we & (offset == PTP_CMD // 4) & self.bus.dat_w[PTP_SNAPSHOT_BIT],
                         tod.eq(now_ns))]
        self.comb += If(held == TOD_RD[0] // 4, self.bus.dat_r.eq(tod[:32])).Elif(
            held == TOD_RD[1] // 4, self.bus.dat_r.eq(tod[32:])).Else(self.bus.dat_r.eq(rd.dat_r))


def hook_pads(n_if: int) -> list:
    """The counter-change event's pads: its pulse and its descriptor, per interface."""
    return [('hook', 0, Subsignal('ctr_chg', Pins(n_if)), Subsignal('ctr_type', Pins(16 * n_if)),
             Subsignal('ctr_index', Pins(16 * n_if)))]


def window_answer(module: LiteXModule, face: dict, window: object, n_if: int) -> dict:
    """One window's answers at its bound: each interface's open request answered by a one-cycle pulse with its
    tag, wait_cycles - 1 cycles after it opened (KL_mbx accepts an answer up to that cycle). CTR answers word w
    of a change's descriptor with (changes on that interface << 8) | w, and counters_valid (word 32) with every
    bit; GSI answers 3 to the format verdict (selector 15) and 0 to every other word."""
    lw = window.name.lower()
    req = face[f'o_{lw}_req_o']
    tag = face[f'o_{lw}_tag_o']
    tag_w = len(tag) // n_if
    data_w = 32 if window.name == 'CTR' else 64
    pulse = Signal(n_if)
    tags = Signal(n_if * tag_w)
    data = Signal(n_if * data_w)
    last = window.wait_cycles - 1
    for i in range(n_if):
        waited = Signal(max=window.wait_cycles)
        module.sync += If(~req[i], waited.eq(0)).Elif(waited != last, waited.eq(waited + 1))
        module.comb += [pulse[i].eq(req[i] & (waited == last)),
                        tags[i * tag_w:(i + 1) * tag_w].eq(tag[i * tag_w:(i + 1) * tag_w])]
        if window.name == 'CTR':
            word = face['o_ctr_word_o'][6 * i:6 * (i + 1)]
            module.comb += If(word == 32, data[32 * i:32 * (i + 1)].eq(0xFFFFFFFF)).Else(
                data[32 * i:32 * (i + 1)].eq((module.changes[16 * i:16 * (i + 1)] << 8) | word))
        else:
            sel = face['o_gsi_sel_o'][4 * i:4 * (i + 1)]
            module.comb += If(sel == 15, data[64 * i:64 * (i + 1)].eq(3)).Else(data[64 * i:64 * (i + 1)].eq(0))
    return {f'i_{lw}_ans_p_i': pulse, f'i_{lw}_ans_tag_i': tags, f'i_{lw}_ans_data_i': data}


class FaceDrive(LiteXModule):
    """The answering arm's datapath side of the face block: the CTR and GSI windows answered at their bound, and
    the counter-change event from the testbench's pads, counted per interface."""

    def __init__(self, pads: object, n_if: int) -> None:
        self.pads = pads
        self.n_if = n_if
        self.changes = Signal(16 * n_if)
        for i in range(n_if):
            self.sync += If(pads.ctr_chg[i], self.changes[16 * i:16 * (i + 1)].eq(
                self.changes[16 * i:16 * (i + 1)] + 1))

    def inputs(self, face: dict, contract: object) -> dict:
        """The face inputs this arm drives instead of holding them idle."""
        driven = dict(i_ctr_chg_p_i=self.pads.ctr_chg, i_ctr_chg_type_i=self.pads.ctr_type,
                      i_ctr_chg_index_i=self.pads.ctr_index)
        for window in contract.face_windows:
            if window.name in ANSWERED:
                driven.update(window_answer(self, face, window, self.n_if))
        return driven


def face_patch(arm: str, drive: FaceDrive, contract: object) -> object:
    """split_soc.face_ports, which StimulusMailbox connects, with the arm's inputs: unchanged for `idle`."""
    original = split_soc.face_ports
    if arm == 'idle':
        return patch.object(split_soc, 'face_ports', original)

    def ports(c: object, n_if: int) -> dict:
        """The CPU budget harness's face ports, with the arm's inputs in place of the idle ones."""
        face = original(c, n_if)
        return {**face, **drive.inputs(face, contract)}
    return patch.object(split_soc, 'face_ports', ports)


@dataclasses.dataclass(frozen=True)
class Build:
    """One export's selection: the shape, its interfaces, the linked image, the face arm, the CPU clock (None
    for the shape's Milan clock, the product's) and the ledgered point the SoC's memory plan is held to."""

    shape: str
    n_if: int
    elf: Path
    arm: str = 'idle'
    cpu_hz: int | None = None
    ledgered: str | None = None

    def __post_init__(self) -> None:
        if self.arm not in ARMS:
            raise RuntimeError(f'unknown face arm {self.arm!r}')


def build(build_dir: Path, sel: Build) -> dict:
    """Export the SoC's Verilog and csr.csv; return the native build's inputs."""
    addresses = split_soc.fixture_addresses()
    cfg = capture_soc.eb.load_config(str(ROOT / 'configs' / (sel.shape + '.yaml')))
    clocks, params = cfg['constraints'], cfg['soc']
    contract = milan_soc.ctrl_mailbox_contract()
    deviations = split_soc.ack_deviations(contract)
    if deviations:
        raise RuntimeError(f'the commit acknowledgement is not at the contract bound: {deviations}')
    platform = split_soc.platform_for(contract, sel.n_if)
    platform.add_extension(hook_pads(sel.n_if))
    cpu = split_soc.CpuPatches('cover')
    geometry = split_soc.fetch_l1_geometry('split')
    scala_args = [*params['scala_args'], *filter(None, [milan_soc.ctrl_cpu_args(geometry)])]
    sys_hz = clocks['sys_clk_hz']
    product_hz = clocks['milan_clk_hz']
    cpu_hz = product_hz if sel.cpu_hz is None else sel.cpu_hz
    from mailbox_model import with_interfaces
    drive = FaceDrive(platform.request('hook'), sel.n_if)
    with cpu.applied(), split_soc.ledgered_plan(sel.ledgered), face_patch(sel.arm, drive,
                                                                          with_interfaces(contract, sel.n_if)):
        soc = milan_soc.MilanSoC(
            platform, sys_hz, xlen=params['xlen'], cpu_count=params['cpu_count'], cpu=params['cpu'],
            board='ax7101', with_milan=False, with_mac=False, with_dram=False, with_spiflash=False,
            flashboot=clocks['flashboot'], milan_clk_freq=cpu_hz, l2_bytes=clocks['l2_bytes'],
            extra_scala_args=scala_args, uart_name='sim', uart_baudrate=clocks['uart_baudrate'],
            integrated_rom_size=0, integrated_sram_size=0, integrated_main_ram_size=0, with_timer=False)
        milan_soc.add_ctrl_memory(soc, sel.elf)
        for path in split_soc.mailbox_sources(sel.n_if, build_dir / 'mbx-variant'):
            platform.add_source(str(path))
        split_soc.add_devices(soc, platform, addresses, contract, sel.n_if)
        soc.face_drive = drive
        soc.milan_csr = CsrFile(milan_soc.MILAN_CSR_SIZE, sys_hz)
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
        'sys_hz': sys_hz, 'cpu_hz': cpu_hz, 'product_cpu_hz': product_hz,
        'cpu_clock': 'product' if cpu_hz == product_hz else 'variant',
        'shape': sel.shape, 'interfaces': sel.n_if, 'arm': sel.arm, 'ledgered': sel.ledgered,
        'addresses': addresses, 'window_bytes': contract.window_bytes,
        'csr_base': milan_soc.MILAN_CSR_BASE, 'csr_size': milan_soc.MILAN_CSR_SIZE,
        'netlist': VexiiRiscv.netlist_name,
        'memory_regions': cpu.soc_regions, 'cpu_regions': 'cover',
        'cpu_memory_regions': [list(r) for r in VexiiRiscv.memory_regions],
        'fetch_l1': 'split', 'fetch_l1_geometry': list(geometry) if geometry else None,
        'ctrl_plan': soc.ctrl_plan.summary(),
    }
    (build_dir / 'soc.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec
