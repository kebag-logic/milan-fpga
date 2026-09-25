"""Check the product SoC on simulated clocks and memory devices."""
import argparse
import binascii
import json
from pathlib import Path
import sys
from unittest.mock import patch

from migen import ClockDomain, ClockSignal, Module, ResetSignal
from litex.build.generic_platform import Pins
from litex.gen import LiteXModule
from litex.build.sim.config import SimConfig
from litex.soc.integration.builder import Builder
from litex.tools.litex_sim import Platform
from litedram.modules import MT41J256M16
from litedram.phy import s7ddrphy
from litedram.phy.model import SDRAMPHYModel
from litespi.phy.model import LiteSPIPHYModel

ROOT = Path('$LANES/559-capture-copy')
SCRATCH = Path('$VALIDATION_STORAGE/559-a307-product-preflight')
sys.path[:0] = [str(ROOT / 'sw/litex'), str(ROOT / 'sw/builder')]
import milan_soc
import endstation_builder as eb
from platforms.alinx_ax7101 import _io

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
                      self.cd_audio_tdm.clk.eq(ClockSignal('audio')),
                      self.cd_milan.rst.eq(ResetSignal('sys')),
                      self.cd_audio.rst.eq(ResetSignal('sys'))]


def model_phy(pads, **kwargs):
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

    def add_spi_flash(self, **kwargs):
        self.spiflash_phy = LiteSPIPHYModel(kwargs['module'], init=self.flash_image)
        kwargs['phy'] = self.spiflash_phy
        return super().add_spi_flash(**kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--shape', default='endstation_ax7101_8x8')
    parser.add_argument('--compile', action='store_true')
    args = parser.parse_args()
    cfg = ROOT / 'configs' / (args.shape + '.yaml')
    # Pure derivation and output emission, avoiding tracked generated headers.
    art = eb._derive_artifacts(str(cfg))
    generated, outputs = eb._write_artifact_dir(art, str(SCRATCH / 'generated'))
    generated = Path(generated)
    platform = Platform()
    platform.add_extension([entry for entry in _io if entry[0] == 'ddram'])
    platform.add_extension([('milan_clk', 0, Pins(1)), ('audio_clk', 0, Pins(1)),
                            ('sys_reset', 0, Pins(1))])
    config = art.cfg
    clocks = config['constraints']
    params = config['soc']
    with patch.object(milan_soc, '_CRG', SimClocks), \
         patch.object(s7ddrphy, 'A7DDRPHY', model_phy), \
         patch.object(milan_soc, '_builder_out', lambda _, name: str(generated / name)):
        blob, report, overlay_path = milan_soc.build_desc_image(str(generated))
        flash = bytearray(b'\xff' * milan_soc.FLASH_SIZE)
        aem_offset = milan_soc.FLASHBOOT_AEM['offset']
        flash[aem_offset:aem_offset + len(blob)] = blob
        ProductSimulation.flash_image = [int.from_bytes(flash[i:i+4], 'little')
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
            talker_wire_chans=eb.framer_wire_channels(config),
            optional_blocks={name: eb.block_present(config, name)
                             for name in milan_soc.MILAN_OPTIONAL_BLOCKS},
            render_lpf=eb.block_present(config, 'render_lpf'),
            uart_name='sim', uart_baudrate=clocks['uart_baudrate'],
        )
        soc.add_config('BIOS_NO_CRC')
        soc.add_config('BIOS_NO_DELAYS')
        soc.add_constant('SDRAM_TEST_DISABLE')
        soc.add_constant('MILAN_AEM_FLASH_OFFSET', aem_offset)
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
        shape = milan_soc.NvmShape(cfg=cfg, names=int.from_bytes(blob[10:12], 'big'),
            dc=overlay['descriptor_counts'], spi=overlay['stream_ports']['input'],
            spo=overlay['stream_ports']['output'])
        donor = milan_soc.NvmDonor(base=milan_soc.binding_base(), layout=milan_soc.layout_version())
        for name, value in milan_soc.firmware_constants(shape, donor).items():
            soc.add_constant(name, value)
        builder = Builder(soc, output_dir=str(SCRATCH / args.shape),
                          compile_software=args.compile, compile_gateware=False)
        from measurement_firmware import prepare
        firmware = prepare(ROOT, SCRATCH / args.shape / 'measurement_firmware')
        builder.add_software_package('libmilan_baremetal', str(firmware))
        builder.add_software_library('libmilan_baremetal', always_link=True)
        sim_config = SimConfig()
        sim_config.add_clocker('sys_clk', freq_hz=clocks['sys_clk_hz'])
        sim_config.add_clocker('milan_clk', freq_hz=clocks['milan_clk_hz'])
        sim_config.add_clocker('audio_clk', freq_hz=24576000)
        sim_config.add_module('serial2console', 'serial')
        builder.build(run=False, sim_config=sim_config, jobs=8, opt_level='O3')
        (SCRATCH / args.shape / 'sources.json').write_text(json.dumps({
            'sources': [str(Path(s[0]).resolve()) for s in soc.platform.sources],
            'includes': soc.platform.verilog_include_paths,
            'sys_hz': clocks['sys_clk_hz'], 'cpu_hz': clocks['milan_clk_hz'],
        }, indent=2))
    print('PRODUCT_LOGICAL_SOC_ELABORATED', flush=True)


if __name__ == '__main__':
    main()
