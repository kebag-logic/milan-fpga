"""Exercise the installed wrapper's product CPU metadata generator offline."""
import argparse
from pathlib import Path

from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
import pythondata_cpu_vexiiriscv

parser = argparse.ArgumentParser()
VexiiRiscv.args_fill(parser)
args = parser.parse_args([])
# sw/litex/milan_soc.py:2552-2579, for either assigned board shape.
args.cpu_variant = "baremetal"
args.cpu_count = 1
args.with_dma = True
args.with_cpu_clk = True
args.l2_bytes = 0
args.vexii_args = "--xlen=32"
args.update_repo = "no"
print("Board CPU setup: cacheless RV32I, one hart, DMA, CPU clock CDC, no L2", flush=True)
print("Data tree:", Path(pythondata_cpu_vexiiriscv.data_location), flush=True)
VexiiRiscv.args_read(args)
print("PRODUCT_CPU_METADATA_READY", flush=True)
print("XLEN:", VexiiRiscv.xlen, "ISA:", VexiiRiscv.isa_map, flush=True)
