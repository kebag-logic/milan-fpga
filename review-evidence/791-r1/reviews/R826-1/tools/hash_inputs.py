"""hash_inputs.py <clone> <build-dir> <shape> <elf> <mutant>: region_soc.build with LiteX's netlist naming
inputs printed (each soc_args field and the other hashed fields), and generation refused, so the cache is
never written."""
import sys
from pathlib import Path
clone = Path(sys.argv[1])
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_region_decode'))
import region_soc
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
orig = VexiiRiscv.generate_netlist_name
def show():
    for k, v in vars(VexiiRiscv.soc_args).items():
        print('SOC_ARG', k, repr(v))
    for k in ('reset_address', 'litedram_width', 'xlen', 'memory_regions', 'vexii_args', 'with_opensbi', 'with_supervisor'):
        print('FIELD', k, repr(getattr(VexiiRiscv, k)))
    orig()
    print('NAME', VexiiRiscv.netlist_name)
    raise SystemExit(0)
VexiiRiscv.generate_netlist_name = staticmethod(show)
def refuse(*a, **k):
    raise SystemExit('generation refused')
VexiiRiscv.generate_netlist = staticmethod(refuse)
region_soc.build(Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4]).resolve(), sys.argv[5])
