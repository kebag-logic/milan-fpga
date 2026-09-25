"""Elaborate the product CPU and DDR bus on the installed simulation platform."""
from pathlib import Path
import sys

from migen import ClockDomain, ClockSignal
from litex.soc.integration.builder import Builder
from litex.build.sim.config import SimConfig
from litex.tools.litex_sim import SimSoC

from cpu_preflight import VexiiRiscv

root = Path("$LANES/559-capture-copy")
sys.path.insert(0, str(root / "sw/litex"))
from milan_soc import cross_cpu_memory_ports


class PreflightSoC(SimSoC):
    def add_sdram(self, *args, **kwargs):
        self.cd_milan = ClockDomain("milan")
        self.comb += self.cd_milan.clk.eq(ClockSignal("sys"))
        self.comb += self.cpu.cpu_clk.eq(ClockSignal("milan"))
        cross_cpu_memory_ports(self.cpu, cd_from="milan", cd_to="sys")
        return super().add_sdram(*args, **kwargs)


soc = PreflightSoC(
    cpu_type="vexiiriscv", cpu_variant="baremetal", cpu_count=1,
    bus_standard="axi-lite", uart_name="sim", integrated_rom_size=0x20000,
    integrated_main_ram_size=0, with_sdram=True, sdram_module="MT41J256M16",
    sdram_data_width=32, l2_size=0,
)
builder = Builder(soc, output_dir="$VALIDATION_STORAGE/559-a307-cpu-preflight/soc",
                  compile_software="--compile" in sys.argv, compile_gateware=False)
config = SimConfig()
config.add_clocker("sys_clk", freq_hz=100000000)
config.add_module("serial2console", "serial")
builder.build(run=False, sim_config=config, jobs=8)
print("PRODUCT_CPU_SOC_ELABORATED", flush=True)
