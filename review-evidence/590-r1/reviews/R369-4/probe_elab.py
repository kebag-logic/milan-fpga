#!/usr/bin/env python3
"""Probe P1: elaborate the capture-simulation SoC to Verilog without compiling.

Run from a checkout root with a LiteX interpreter carrying the patch series:
  probe_elab.py <shape> <build-dir>
The capture harness's own build() (tb/verilator/nvm_capture_cpu/soc.py) is
called unchanged, except that Builder compiles no software and the platform
writes its Verilog and sim sources but its Verilator compile step is skipped. The result is the generated
gateware and software headers, which a caller diffs across two trees.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'tb/verilator/nvm_capture_cpu'))
import soc as capture_soc  # noqa: E402

Builder = capture_soc.Builder
original_init = Builder.__init__


def init(self, soc, **kwargs):
    kwargs['compile_software'] = False
    original_init(self, soc, **kwargs)


def skip_compile(**kwargs):
    print('sim compile skipped:', kwargs.get('build_name'))


original_includes = Builder._generate_includes


def includes(self, with_bios=True):
    # The pins-only interpreter carries no firmware data package; omit only
    # the BIOS make variables, as sw/builder/test_shipping_clock_constraints.py does.
    original_includes(self, with_bios=False)


Builder.__init__ = init
import litex.build.sim.verilator as sim_verilator  # noqa: E402
sim_verilator._build_sim = skip_compile
# The make-variable file needs a data package the pins-only install lacks.
sim_verilator._generate_sim_variables = lambda *a, **k: None
Builder._generate_includes = includes
args = argparse.Namespace(shape=sys.argv[1], build_dir=Path(sys.argv[2]).resolve(),
                          captures=16, cpu_hz=50_000_000, traffic='on', mutation='none')
capture_soc.build(args)
print('elaborated', args.shape, args.build_dir)
