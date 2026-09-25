# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Product SoC with simulated clocks/devices and its unchanged memory buses."""
import argparse
import binascii
import json
from pathlib import Path
import sys
from unittest.mock import patch

from migen import ClockDomain, ClockSignal, ResetSignal
from litex.build.generic_platform import Pins
from litex.gen import LiteXModule
from litex.build.sim.config import SimConfig
from litex.soc.integration.builder import Builder
from litex.tools.litex_sim import Platform
from litedram.modules import MT41J256M16
from litedram.phy import s7ddrphy
from litedram.phy.model import SDRAMPHYModel
from litespi.phy.model import LiteSPIPHYModel

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'sw/litex'), str(ROOT / 'sw/builder')]
import milan_soc
import endstation_builder as eb
from platforms.alinx_ax7101 import _io
from probe import CaptureProbe, add_pads, packet_ports

REAL_PHY = s7ddrphy.A7DDRPHY


class SimClocks(LiteXModule):
    def __init__(self, platform, sys_clk_freq, **kwargs):
        self.cd_sys = ClockDomain('sys')
        self.cd_milan = ClockDomain('milan')
        self.cd_audio = ClockDomain('audio')
        self.cd_audio_tdm = ClockDomain('audio_tdm')
        self.comb += [self.cd_sys.clk.eq(platform.request('sys_clk')),
                      self.cd_sys.rst.eq(platform.request('sys_reset')),
                      self.cd_milan.clk.eq(platform.request('milan_clk')),
                      self.cd_audio.clk.eq(platform.request('audio_clk')),
                      self.cd_audio_tdm.clk.eq(platform.request('audio_tdm_clk')),
                      self.cd_milan.rst.eq(ResetSignal('sys')),
                      self.cd_audio.rst.eq(ResetSignal('sys')),
                      self.cd_audio_tdm.rst.eq(ResetSignal('sys'))]


def model_phy(pads: object, **kwargs: object) -> SDRAMPHYModel:
    """Retain the board PHY's controller-facing latency and phase settings."""
    board_phy = REAL_PHY(pads, **kwargs)
    settings = board_phy.settings
    for attr in ('rdphase', 'wrphase'):
        setattr(settings, attr, int(getattr(settings, attr).reset.value))
    settings.phytype = 'SDRAMPHYModel'
    for attr in ('write_leveling', 'write_dq_dqs_training',
                 'write_latency_calibration', 'read_leveling'):
        setattr(settings, attr, False)
    module = MT41J256M16(kwargs['sys_clk_freq'], '1:4')
    return SDRAMPHYModel(module, settings=settings, clk_freq=kwargs['sys_clk_freq'])


class ProductSimulation(milan_soc.MilanSoC):
    flash_image = []

    def add_spi_flash(self, **kwargs: object) -> object:
        """Retain the product flash controller; replace its serial device."""
        self.spiflash_phy = LiteSPIPHYModel(kwargs['module'], init=self.flash_image)
        kwargs['phy'] = self.spiflash_phy
        return super().add_spi_flash(**kwargs)


def _firmware_constants(soc, args, generated, blob, overlay_path):
    """Publish the same product constants as the board entry, plus probe count."""
    soc.add_config('BIOS_NO_CRC')
    soc.add_config('BIOS_NO_DELAYS')
    soc.add_constant('SDRAM_TEST_DISABLE')
    soc.probe = CaptureProbe(soc.platform, soc.descmem_wb)
    soc.csr.add('probe')
    soc.add_constant('PROBE_CAPTURES', args.captures)
    soc.add_constant('MILAN_AEM_FLASH_OFFSET', milan_soc.FLASHBOOT_AEM['offset'])
    soc.add_constant('MILAN_AEM_IMAGE_BYTES', len(blob))
    soc.add_constant('MILAN_AEM_IMAGE_CRC32', binascii.crc32(blob) & 0xffffffff)
    soc.add_constant('MILAN_AEM_DESC_BASE', soc._pp_windows['desc_base'])
    overlay = json.loads(Path(overlay_path).read_text())
    srp = json.loads((generated / 'lwsrp_table.json').read_text())
    for name, value in milan_soc.fabric_constants(overlay, srp).items():
        soc.add_constant(name, value)
    soc.add_constant('MILAN_NVM_LIVE_BASE', soc._pp_windows['nvm_base'])
    soc.add_constant('MILAN_NVM_STAGE_BASE', soc._pp_windows['nvm_stage_base'])
    soc.add_constant('MILAN_NVM_CONTRACT', 3)
    soc.add_constant('MILAN_NVM_IMAGE_MAX', milan_soc.FLASH_ERASE_BLOCK)
    shape = milan_soc.NvmShape(cfg=ROOT / 'configs' / (args.shape + '.yaml'),
        names=int.from_bytes(blob[10:12], 'big'),
        dc=overlay['descriptor_counts'], spi=overlay['stream_ports']['input'],
        spo=overlay['stream_ports']['output'])
    donor = milan_soc.NvmDonor(base=milan_soc.binding_base(), layout=milan_soc.layout_version())
    for name, value in milan_soc.firmware_constants(shape, donor).items():
        soc.add_constant(name, value)


def build(args: argparse.Namespace) -> Path:
    """Elaborate the selected product and compile the instrumented product firmware."""
    cfg = ROOT / 'configs' / (args.shape + '.yaml')
    # Pure derivation and output emission, avoiding tracked generated headers.
    art = eb._derive_artifacts(str(cfg))
    generated, _outputs = eb._write_artifact_dir(art, str(args.build_dir / 'generated'))
    generated = Path(generated)
    # The RTL includes gen/adp_shape_defaults.svh, not the report at its root.
    # Publish this generated include locally, never transfer the tracked shape's ownership.
    (generated / 'gen').mkdir(exist_ok=True)
    (generated / 'gen/adp_shape_defaults.svh').write_text(art.adp_svh)
    platform = Platform()
    platform.add_extension([entry for entry in _io if entry[0] == 'ddram'])
    platform.add_extension([('milan_clk', 0, Pins(1)), ('audio_clk', 0, Pins(1)),
                            ('audio_tdm_clk', 0, Pins(1)), ('sys_reset', 0, Pins(1))])
    add_pads(platform)
    config = art.cfg
    clocks = config['constraints']
    params = config['soc']
    with patch.object(milan_soc, '_CRG', SimClocks), \
         patch.object(s7ddrphy, 'A7DDRPHY', model_phy), \
         patch.object(milan_soc, '_board_audio_ports', packet_ports), \
         patch.object(milan_soc, '_builder_out', lambda _, name: str(generated / name)):
        blob, report, overlay_path = milan_soc.build_desc_image(str(generated))
        flash = bytearray(b'\xff' * milan_soc.FLASH_SIZE)
        aem_offset = milan_soc.FLASHBOOT_AEM['offset']
        flash[aem_offset:aem_offset + len(blob)] = blob
        # LiteSPI's little-endian memory-map port reverses serial-order words.
        ProductSimulation.flash_image = [int.from_bytes(flash[i:i+4], 'big')
                                        for i in range(0, len(flash), 4)]
        soc = ProductSimulation(
            platform, clocks['sys_clk_hz'], xlen=params['xlen'],
            cpu_count=params['cpu_count'], cpu=params['cpu'], board='ax7101',
            with_milan=True, with_mac=False, with_dram=True, with_spiflash=True,
            flashboot=clocks['flashboot'], milan_clk_freq=clocks['milan_clk_hz'],
            l2_bytes=clocks['l2_bytes'], extra_scala_args=params['scala_args'],
            entity_gen_dir=str(generated), gptp_plane=True,
            gptp_ingress_lat_ns=config['gptp']['ingress_latency_ns'],
            gptp_egress_lat_ns=config['gptp']['egress_latency_ns'],
            num_streams=max(len(config['listeners']), len(config['talkers'])),
            audio_if_slots=eb.audio_if_slots(config),
            audio_if_master=bool(eb.audio_if_slots(config)) and eb.tdm_bus_master(),
            audio_if_render=eb.render_slots(config),
            audio_fs_hz=config['clocking']['sampling_rate_hz'],
            audio_word_bits=eb.tdm_slot_bits(config) or milan_soc.AUDIO_IF_WORD_BITS_DEFAULT,
            loopback_lane=config['interface']['cluster_fabric']['loopback_lane'],
            talker_wire_chans=eb.framer_wire_channels(config),
            optional_blocks={name: eb.block_present(config, name)
                             for name in milan_soc.MILAN_OPTIONAL_BLOCKS},
            render_lpf=eb.block_present(config, 'render_lpf'),
            uart_name='sim', uart_baudrate=clocks['uart_baudrate'],
        )
        _firmware_constants(soc, args, generated, blob, overlay_path)
        builder = Builder(soc, output_dir=str(args.build_dir),
                          compile_software=True, compile_gateware=False)
        from firmware import prepare
        firmware = prepare(ROOT, args.build_dir / 'measurement_firmware', args.mutation)
        builder.add_software_package('libmilan_baremetal', str(firmware))
        builder.add_software_library('libmilan_baremetal', always_link=True)
        sim_config = SimConfig()
        sim_config.add_clocker('sys_clk', freq_hz=clocks['sys_clk_hz'])
        sim_config.add_clocker('milan_clk', freq_hz=clocks['milan_clk_hz'])
        sim_config.add_clocker('audio_clk', freq_hz=24576000)
        tdm_hz = 2 * eb.audio_if_slots(config) * eb.tdm_slot_bits(config) * config['clocking']['sampling_rate_hz']
        sim_config.add_clocker('audio_tdm_clk', freq_hz=tdm_hz or 24576000)
        sim_config.add_module('serial2console', 'serial')
        builder.build(run=False, sim_config=sim_config, jobs=8, opt_level='O3')
        (args.build_dir / 'sources.json').write_text(json.dumps({
            'sources': [str(Path(s[0]).resolve()) for s in soc.platform.sources],
            'includes': soc.platform.verilog_include_paths,
            'sys_hz': clocks['sys_clk_hz'], 'cpu_hz': clocks['milan_clk_hz'],
            'tdm_hz': tdm_hz or 24576000, 'shape': args.shape, 'captures': args.captures,
            'mutation': args.mutation,
        }, indent=2))
    return args.build_dir
