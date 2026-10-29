#!/usr/bin/env python3
"""Scratch: the split CPU and its firmware memory as one Verilog top, for an out-of-context route.

The harness's test SoC (split_soc.build) without its devices: MilanSoC's VexiiRiscv path with the split
placement's options (milan_soc.ctrl_cpu_args), the DMA port, the CPU on its own clock (the top's milan_clk port)
behind the generator's crossings, and rom and sram built from a linked image by milan_soc.add_ctrl_memory on the
bus clock (sys_clk). The CPU generator is handed the product split export's region list (round 4's
receipts/area/exports.txt, dc8k), so the netlist name, a hash of every generator argument, must come out as the
product's; round 8 prints it and records it (the product export's name is checked separately).

usage: ooc_soc.py CHECKOUT BUILD_DIR ELF
Writes BUILD_DIR/gateware/sim.v (top `sim`) and BUILD_DIR/ooc.json (the netlist name and the plan)."""
import contextlib
import json
import sys
from pathlib import Path
from unittest.mock import patch

CHECKOUT, OUT, ELF = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(CHECKOUT / 'tb/verilator/ctrl_service_budget'))
import split_soc  # noqa: E402
from split_soc import Builder, VexiiRiscv, capture_soc, milan_soc  # noqa: E402

PRODUCT_REGIONS = [[0, 229376, 'rxc', 'p'], [268435456, 229376, 'rwxc', 'p'],
                   [1073741824, 1073741824, 'rwxc', 'm'], [16777216, 16777216, 'r', 'p'],
                   [2415919104, 65536, 'rw', 'p'], [2416967680, 32768, 'rw', 'p'],
                   [4026531840, 65536, 'rw', 'p']]


def main() -> int:
    cfg = capture_soc.eb.load_config(str(CHECKOUT / 'configs' / 'endstation_ax7101_1x1_tdm8.yaml'))
    clocks, params = cfg['constraints'], cfg['soc']
    contract = milan_soc.ctrl_mailbox_contract()
    platform = split_soc.platform_for(contract, 1)
    scala_args = [*params['scala_args'], milan_soc.ctrl_cpu_args(milan_soc.CTRL_FETCH_L1)]
    args_read, netlist_name = VexiiRiscv.args_read, VexiiRiscv.generate_netlist_name

    def shipping_args_read(args: object) -> None:
        args.with_dma = True
        args_read(args)

    def product_regions() -> None:
        VexiiRiscv.memory_regions = [tuple(r) for r in PRODUCT_REGIONS]
        netlist_name()

    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(milan_soc, '_CRG', capture_soc.SimClocks))
        stack.enter_context(patch.object(VexiiRiscv, 'args_read', staticmethod(shipping_args_read)))
        stack.enter_context(patch.object(VexiiRiscv, 'generate_netlist_name', staticmethod(product_regions)))
        soc = milan_soc.MilanSoC(
            platform, clocks['sys_clk_hz'], xlen=params['xlen'], cpu_count=params['cpu_count'], cpu=params['cpu'],
            board='ax7101', with_milan=False, with_mac=False, with_dram=False, with_spiflash=False,
            flashboot=clocks['flashboot'], milan_clk_freq=clocks['milan_clk_hz'], l2_bytes=clocks['l2_bytes'],
            extra_scala_args=scala_args, uart_name='sim', uart_baudrate=clocks['uart_baudrate'],
            integrated_rom_size=0, integrated_sram_size=0, integrated_main_ram_size=0, with_timer=False)
        milan_soc.add_ctrl_memory(soc, ELF)
        # The product's LiteDRAM port (256 bits on the AX7101), through MilanSoC's own crossing to the bus
        # clock (cross_cpu_memory_ports), brought out to pins so nothing on the CPU's memory path is trimmed.
        soc.cpu.add_memory_buses(address_width=32, data_width=256)
        for index, bus in enumerate(soc.cpu.memory_buses):
            platform.add_extension(bus.get_ios(f'mbus{index}'))
            soc.comb += bus.connect_to_pads(platform.request(f'mbus{index}'), mode='master')
        builder = Builder(soc, output_dir=str(OUT), compile_software=False, compile_gateware=False)
        builder.build(run=False)
    name = VexiiRiscv.netlist_name
    (OUT / 'ooc.json').write_text(json.dumps(dict(netlist=name, vexii_args=VexiiRiscv.vexii_args,
                                                  plan=soc.ctrl_plan.summary()), indent=1) + '\n')
    print(f'netlist {name}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
