# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The region-decode test SoC (#791): the split CPU, its firmware memory filling each region, and nothing else.

The CPU is the CPU budget harness's (tb/verilator/ctrl_service_budget/split_soc.py,
imported read only): MilanSoC's own VexiiRiscv path with the DMA port the
shipping image has and the split placement's instruction cache, the CPU at
the Milan clock. Its firmware memory is milan_soc.add_ctrl_memory, which
also hands the CPU generator the split regions as aligned power-of-two
pieces (milan_soc.exact_cpu_decode, ctrl_memory.cpu_regions).

Two things differ from the boot SoCs, both so the test reads the decode alone:

  - the plan gives each region banks that fill its whole power-of-two window
    (window_banks): its decode pieces, then the window's rest. So its last
    word is memory, and so is the word past its end, which the SoC's bus
    decodes to the same slave: only the CPU's own decode can refuse it. The
    shipping plan populates only the image's need (ctrl_memory.plan), and
    answers err past it; the CPU's decode, generated from the region list,
    does not depend on it, and test_ctrl_memory.py grades the err hole;
  - the split SoC's other CPU-visible regions are slaves that answer err, at
    the shipping split SoC's places and in its order (the spiflash window,
    placed by LiteX's allocator as add_spi_flash places it, the Milan CSR
    window and the mailbox), so the CPU generator is handed the region list
    of a split SoC without DDR3, as the Arty's split image is built (#878).

MUTANTS are the planted decodes: `single-mask` hands the generator the SoC's
regions without the split (split_soc.CpuPatches 'as-built'), the decode of
#791; `cover` hands it each region's power-of-two cover, the boot harness's
old workaround, which admits the words past each region's end.

    python3 region_soc.py <build-dir> <shape> <elf> <mutant>
"""
from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import split_soc  # noqa: E402  the CPU budget harness's SoC, read only
from litex.build.sim.config import SimConfig  # noqa: E402
from litex.gen import LiteXModule  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402
from litex.soc.integration.builder import Builder  # noqa: E402
from litex.soc.integration.soc import SoCRegion  # noqa: E402
from litex.soc.interconnect import wishbone  # noqa: E402

milan_soc = split_soc.milan_soc
ctrl_memory = milan_soc.ctrl_memory
capture_soc = split_soc.capture_soc
#: The planted decodes, each a function of the CpuPatches arm and a patch of the shipping split.
MUTANTS = ('none', 'single-mask', 'cover')
#: The CPU's own devices LiteX's VexiiRiscv adds as linker regions, which its PMA decodes as well.
CPU_DEVICES = ('clint', 'plic')


class ErrSlave(LiteXModule):
    """A slave that answers every access with err, for a region the test never reads."""

    def __init__(self) -> None:
        self.bus = wishbone.Interface(data_width=32, address_width=32, addressing='word')
        self.sync += self.bus.err.eq(self.bus.cyc & self.bus.stb & ~self.bus.err)


def window_banks(region: ctrl_memory.Region) -> tuple[int, ...]:
    """Banks filling the region's whole power-of-two window: its decode pieces, then the window's rest."""
    window = 1 << (region.size - 1).bit_length()
    pieces = (*ctrl_memory.decode_pieces(region.origin, region.size),
              *ctrl_memory.decode_pieces(region.end, window - region.size))
    return tuple(size for _, size in pieces)


def full_plan(image: ctrl_memory.Image, **_: object) -> ctrl_memory.Plan:
    """The image's map checked as the shipping plan checks it, then banks filling each region's window."""
    ctrl_memory.check_map(image)
    rom, ram = window_banks(ctrl_memory.ROM), window_banks(ctrl_memory.RAM)
    return ctrl_memory.Plan(ctrl_memory.ROM.size, ctrl_memory.RAM.size, rom, ram,
                            budget=(sum(rom) + sum(ram)) / ctrl_memory.TILE_BYTES)


def mutated(mutant: str) -> contextlib.AbstractContextManager:
    """The shipping split, or under `cover` each region's power-of-two cover in its place."""
    if mutant == 'cover':
        return patch.object(ctrl_memory, 'cpu_regions', split_soc.power_of_two_cover)
    return contextlib.nullcontext()


def build(build_dir: Path, shape: str, elf: Path, mutant: str) -> dict:
    """Export the test SoC's Verilog; return the native build's inputs."""
    if mutant not in MUTANTS:
        raise RuntimeError(f'unknown mutant {mutant}')
    cfg = capture_soc.eb.load_config(str(ROOT / 'configs' / (shape + '.yaml')))
    clocks, params = cfg['constraints'], cfg['soc']
    contract = milan_soc.ctrl_mailbox_contract()
    platform = split_soc.platform_for(contract, 1)
    geometry = split_soc.fetch_l1_geometry('split')
    scala_args = [*params['scala_args'], *filter(None, [milan_soc.ctrl_cpu_args(geometry)])]
    sys_hz, cpu_hz = clocks['sys_clk_hz'], clocks['milan_clk_hz']
    with mutated(mutant), patch.object(ctrl_memory, 'plan', full_plan):
        cpu = split_soc.CpuPatches('as-built' if mutant == 'single-mask' else 'cover')
        with cpu.applied():
            soc = milan_soc.MilanSoC(
                platform, sys_hz, xlen=params['xlen'], cpu_count=params['cpu_count'], cpu=params['cpu'],
                board='ax7101', with_milan=False, with_mac=False, with_dram=False, with_spiflash=False,
                flashboot=clocks['flashboot'], milan_clk_freq=cpu_hz, l2_bytes=clocks['l2_bytes'],
                extra_scala_args=scala_args, uart_name='sim', uart_baudrate=clocks['uart_baudrate'],
                integrated_rom_size=0, integrated_sram_size=0, integrated_main_ram_size=0, with_timer=False)
            milan_soc.add_ctrl_memory(soc, elf)
            for name, origin, size, kind in (
                    ('spiflash', soc.mem_map.get('spiflash'), milan_soc.FLASH_SIZE, dict(mode='rx', cached=True)),
                    ('milan_csr', milan_soc.MILAN_CSR_BASE, milan_soc.MILAN_CSR_SIZE, dict(cached=False)),
                    ('ctrl_mbx', milan_soc.CTRL_MBX_BASE, contract.window_bytes, dict(cached=False))):
                setattr(soc, name, ErrSlave())
                soc.bus.add_slave(name, getattr(soc, name).bus, region=SoCRegion(origin=origin, size=size, **kind))
            builder = Builder(soc, output_dir=str(build_dir), compile_software=False, compile_gateware=False,
                              csr_csv=str(build_dir / 'csr.csv'))
            sim_config = SimConfig()
            sim_config.add_clocker('sys_clk', freq_hz=sys_hz)
            sim_config.add_clocker('milan_clk', freq_hz=cpu_hz)
            builder.build(run=False, sim_config=sim_config)
    spec = {
        'sources': [str(Path(s[0]).resolve()) for s in soc.platform.sources],
        'includes': soc.platform.verilog_include_paths,
        'sys_hz': sys_hz, 'cpu_hz': cpu_hz, 'shape': shape, 'mutant': mutant,
        'netlist': VexiiRiscv.netlist_name,
        'memory_regions': cpu.soc_regions,
        'cpu_memory_regions': [list(r) for r in VexiiRiscv.memory_regions],
        'cpu_devices': [[soc.bus.regions[n].origin, soc.bus.regions[n].size, 'rw', 'p']
                        for n in CPU_DEVICES if n in soc.bus.regions],
        'vexii_args': VexiiRiscv.vexii_args,
        'ctrl_plan': soc.ctrl_plan.summary(),
    }
    (build_dir / 'soc.json').write_text(json.dumps(spec, indent=2) + '\n')
    return spec


if __name__ == '__main__':
    print(json.dumps(build(Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve(), sys.argv[4])))
