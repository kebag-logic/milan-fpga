# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reuse the capture SoC read-only, replacing only measurement boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
CAPTURE = ROOT / 'tb/verilator/nvm_capture_cpu'


def build(args: argparse.Namespace) -> dict:
    """Link the shipping translation unit, with passive bus observation pads."""
    sys.path.insert(0, str(CAPTURE))
    import soc as capture_soc
    import firmware as capture_firmware
    from migen import Signal
    from litex.gen import LiteXModule
    from litex.build.generic_platform import Pins, Subsignal
    from litex.soc.interconnect import stream
    from litespi.common import spi_core2phy_layout, spi_phy2core_layout

    class DeviceBoundary(LiteXModule):
        """Keep the real controller; the native driver models the flash device."""

        def __init__(self, platform: object, flash: object) -> None:
            self.flash = flash
            self.sink = stream.Endpoint(spi_core2phy_layout)
            self.source = stream.Endpoint(spi_phy2core_layout)
            self.cs = Signal()
            self.dummy_bits = Signal(8)
            fields = [('cs', 1), ('tx_valid', 1), ('tx_ready', 1), ('tx_data', 32),
                      ('tx_len', 6), ('tx_width', 4), ('rx_valid', 1), ('rx_ready', 1), ('rx_data', 32)]
            platform.add_extension([('flash', 0, *[Subsignal(n, Pins(w)) for n, w in fields])])
            pads = platform.request('flash')
            self.comb += [pads.cs.eq(self.cs), pads.tx_valid.eq(self.sink.valid),
                          self.sink.ready.eq(pads.tx_ready), pads.tx_data.eq(self.sink.data),
                          pads.tx_len.eq(self.sink.len), pads.tx_width.eq(self.sink.width),
                          self.source.valid.eq(pads.rx_valid), pads.rx_ready.eq(self.source.ready),
                          self.source.data.eq(pads.rx_data)]

    def add_flash(soc: object, **kwargs: object) -> object:
        """Substitute the device endpoint while retaining the product controller."""
        soc.spiflash_phy = DeviceBoundary(soc.platform, kwargs['module'])
        kwargs['phy'] = soc.spiflash_phy
        return capture_soc.milan_soc.MilanSoC.add_spi_flash(soc, **kwargs)

    from phy import PhyBoundary
    original_ports = capture_soc.packet_ports
    phy_boundary = None

    def packet_ports(platform: object) -> tuple[dict, None]:
        """Attach the peer to the same datapath status ports as MilanMAC."""
        nonlocal phy_boundary
        phy_boundary = PhyBoundary(platform)
        ports, unused = original_ports(platform)
        ports.update(phy_boundary.dp_ports)
        return ports, unused

    original_constants = capture_soc._firmware_constants

    def constants(soc: object, options: argparse.Namespace, generated: Path,
                  blob: bytes, overlay_path: Path) -> None:
        """Retain build constants and observe completed product transactions."""
        original_constants(soc, options, generated, blob, overlay_path)
        soc.milan_mac = phy_boundary
        soc.csr.add('milan_mac')
        soc.bus.add_master(name='phy_status_reader', master=phy_boundary.reader)
        (options.build_dir / 'aem_desc.bin').write_bytes(blob)
        # Observe the system-side boundary, including all product CDC latency.
        bus = soc.bus.slaves['milan_csr']
        values = dict(write=bus.cyc & bus.stb & bus.ack & bus.we,
                      address=bus.adr << 2, data=bus.dat_w, error=bus.err)
        req = soc.milan.nvmmem_req_sys
        rsp = soc.milan.nvmmem_rsp_sys
        values.update(nvm_request=req.valid & req.ready,
                      nvm_response=rsp.valid & rsp.ready, nvm_error=rsp.err)
        soc.platform.add_extension([('observe', 0, *[Subsignal(n, Pins(len(v))) for n, v in values.items()])])
        pads = soc.platform.request('observe')
        soc.comb += [getattr(pads, n).eq(v) for n, v in values.items()]

    def firmware_source(root: Path, destination: Path, mutation: str) -> Path:
        """Adapt the shared capture callback to the explicit service control."""
        return prepare_firmware(destination, args.mutation)
    with patch.object(capture_soc.ProductSimulation, 'add_spi_flash', add_flash), \
         patch.object(capture_soc, '_firmware_constants', constants), \
         patch.object(capture_soc, 'packet_ports', packet_ports), \
         patch.object(capture_firmware, 'prepare', side_effect=firmware_source):
        capture_soc.build(args)
    spec = json.loads((args.build_dir / 'sources.json').read_text())
    spec['firmware_sha256'] = hashlib.sha256(
        (ROOT / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_bytes()).hexdigest()
    return spec


def prepare_firmware(destination: Path, mutation: str) -> Path:
    """Retain production bytes except for explicit negative-control mutations."""
    firmware_path = ROOT / 'sw/firmware/milan_baremetal'
    if mutation == 'none':
        return firmware_path
    source = (firmware_path / 'milan_baremetal.c').read_text()
    if mutation == 'remove-dispatch':
        names = ('milan_status', 'milan_nvm', 'milan_gettime', 'milan_settime', 'milan_utc')
        for name in names:
            anchor = f'static void {name}_handler(int nb_params, char **params)\n{{\n\tnvm_heartbeat_tick();'
            if source.count(anchor) != 1:
                raise RuntimeError('dispatch mutation anchor is not unique')
            source = source.replace(anchor, anchor.removesuffix('\n\tnvm_heartbeat_tick();'))
    else:
        anchor = '\tmilan_mac_link_status_write(status);'
        if source.count(anchor) != 1:
            raise RuntimeError('publication mutation anchor is not unique')
        source = source.replace(anchor, '\t(void)status;')
        source = source.replace('milan_mac_link_status_write(0);', '(void)0;')
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'milan_baremetal.c').write_text(source)
    (destination / 'Makefile').write_bytes((firmware_path / 'Makefile').read_bytes())
    return destination


def compile_sim(build_dir: Path, spec: dict) -> None:
    """Compile the unchanged product hierarchy and the external device driver."""
    header = '#pragma once\n#include <cstdint>\n'
    for name in ('sys_hz', 'cpu_hz', 'tdm_hz'):
        header += f'constexpr std::uint64_t {name} = {spec[name]};\n'
    (build_dir / 'probe_config.hpp').write_text(header)
    retirement_header(build_dir, spec)
    argv = ['verilator', '--cc', '--exe', '--build', '-j', '8', '-Wno-fatal', '-Werror-USERERROR',
            '-Wno-BLKANDNBLK', '-Wno-WIDTH', '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE',
            '--top-module', 'sim', '--Mdir', str(build_dir / 'native'), '-O3',
            '--output-split', '5000', '--output-split-cfuncs', '500',
            '-CFLAGS', f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{build_dir}',
            *['-I' + str(i) for i in spec['includes']], str(Path(__file__).with_name('observe.vlt')),
            *spec['sources'],
            str(Path(__file__).with_name('sim_main.cpp'))]
    subprocess.run(argv, cwd=build_dir / 'gateware', check=True)


def retirement_header(build_dir: Path, spec: dict) -> None:
    """Bind passive retirement observation to the linked ELF and CPU instance."""
    triple = os.environ['LITEX_ENV_CC_TRIPLE']
    symbols = subprocess.check_output([triple + '-nm', str(build_dir / 'software/bios/bios.elf')], text=True)
    matches = re.findall(r'^([0-9a-f]+) t nvm_heartbeat_tick$', symbols, re.M)
    if len(matches) != 1:
        raise RuntimeError('heartbeat entry must have exactly one linked symbol')
    wrappers = [Path(p).stem for p in spec['sources'] if Path(p).stem.startswith('VexiiRiscvLitex_')]
    if len(wrappers) != 1:
        raise RuntimeError('expected one shipping CPU wrapper')
    wrapper = wrappers[0]
    header = f'''#pragma once
#include "Vsim___024root.h"
#include "Vsim_sim.h"
#include "Vsim_{wrapper}.h"
#include "Vsim_VexiiRiscv.h"
inline bool heartbeat_entry(const Vsim& dut) {{
    const auto& cpu = *dut.rootp->sim->{wrapper}->vexiis_0_logic_core;
    return cpu.WhiteboxerPlugin_logic_commits_ports_0_valid
        && cpu.WhiteboxerPlugin_logic_commits_ports_0_pc == 0x{matches[0]}u;
}}
'''
    (build_dir / 'retirement.hpp').write_text(header)
