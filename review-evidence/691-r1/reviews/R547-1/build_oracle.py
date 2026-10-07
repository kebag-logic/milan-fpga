#!/usr/bin/env python3
"""Emit old and patched receivers from dependency sources for an edge-level oracle."""
import importlib.util
from pathlib import Path
import sys
import types
from migen.fhdl import verilog

repo=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
scratch=packet/'scratch'
spec=importlib.util.spec_from_file_location('capture_test',repo/'sw/litex/test_gmii_rx_capture.py')
bench=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)
for name in ('candidate','original'):
    module=types.ModuleType('review_receiver')
    exec(compile((scratch/f'gmii-{name}.py').read_text(),name,'exec'),module.__dict__)
    bench.LiteEthPHYGMIIRX=module.LiteEthPHYGMIIRX
    dut=bench.CaptureBench()
    ports={dut.cd_sys.clk,dut.reset,dut.pads.rx_dv,dut.pads.rx_data,
           dut.rx.source.valid,dut.rx.source.data,dut.rx.source.last}
    verilog.convert(dut,ios=ports,name=f'gmii_{name}').write(str(scratch/f'{name}.v'))
(scratch/'oracle_top.sv').write_text('''module oracle_top(
input clk, rst, pad_valid, input [7:0] pad_data,
output new_valid, new_last, old_valid, old_last,
output [7:0] new_data, old_data);
gmii_candidate a(.sys_clk(clk),.reset(rst),.pads_rx_dv(pad_valid),.pads_rx_data(pad_data),
  .source_valid(new_valid),.source_last(new_last),.source_payload_data(new_data));
gmii_original b(.sys_clk(clk),.reset(rst),.pads_rx_dv(pad_valid),.pads_rx_data(pad_data),
  .source_valid(old_valid),.source_last(old_last),.source_payload_data(old_data));
endmodule
''')
print('PASS: both independent upstream receiver sources emitted')
