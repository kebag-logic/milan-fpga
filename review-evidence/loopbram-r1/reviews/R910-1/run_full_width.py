#!/usr/bin/env python3
"""Expand the exact-head wire fixture to eight concurrent output streams."""
import argparse, pathlib, subprocess, json
p=argparse.ArgumentParser(); p.add_argument('source',type=pathlib.Path); p.add_argument('--simulator',required=True); a=p.parse_args()
out=pathlib.Path(__file__).resolve().parent/'scratch'/'full-width'; out.mkdir(exist_ok=True)
tb=a.source/'tb/verilator/input_loopback'
w=(tb/'loopback_wrap.sv').read_text()
w=w.replace('input wire [2:0] out_addr_i','input wire [5:0] out_addr_i').replace('.N_SLOTS_P(4)', '.N_SLOTS_P(32)').replace('.N_LB_STREAMS_P(1)', '.N_LB_STREAMS_P(8)').replace('.N_LB_CH_P(2)', '.N_LB_CH_P(8)').replace('.N_TALKERS_P(1)', '.N_TALKERS_P(8)').replace(".stream_en_i(1'b1)",".stream_en_i(8'hff)")
(out/'loopback_wrap.sv').write_text(w)
c=(tb/'sim_main.cpp').read_text()
c=c.replace('#include "../../common/verilator_harness.hpp"','#include "'+str(a.source/'tb/common/verilator_harness.hpp')+'"')
c=c.replace('std::array<uint32_t, 8>', 'std::array<uint32_t, 64>').replace('std::array<int, 8> outputs', 'std::array<int, 64> outputs')
c=c.replace('std::deque<Frame> expected_wire;', 'std::array<std::deque<Frame>, 8> expected_wire;')
c=c.replace('for(int c=0;c<8;++c) {\n            int dest', 'for(int c=0;c<64;++c) {\n            int dest')
c=c.replace('check(expected_wire.size()>=6', 'int t=wire[payload-13];\n        check(t<8,"WIRE_STREAM");\n        check(expected_wire[t].size()>=6')
c=c.replace('expected_wire.size()>=6', 'expected_wire[t].size()>=6')
c=c.replace('expected_wire.front(); expected_wire.pop_front();','expected_wire[t].front(); expected_wire[t].pop_front();').replace('want[c],"WIRE_SAMPLE",got,want[c]', 'want[8*t+c],"WIRE_SAMPLE",got,want[8*t+c]')
c=c.replace('expected_wire.push_back(expected);','for(auto& q:expected_wire) q.push_back(expected);')
c=c.replace('check(c<8,"PAIR_INDEX")','check(c<64,"PAIR_INDEX")').replace('if(c<8) {','if(c<64) {')
c=c.replace('for(int c=0;c<8;++c)output(c,c);','for(int c=0;c<64;++c)output(c,c);')
start=c.index('        // Visit every destination,')
end=c.index('        setmap(0,NSTREAMS-1',start)
c=c[:start]+'        // All 63 destinations remain live together; output 63 is invalid.\n'+c[end:]
c=c.replace('bool events = true;', 'bool events = true; int captured = 0;')
c=c.replace('if(phase==300) {expected=predict(frame);', 'if(phase==300) {captured=0; expected=predict(frame);')
c=c.replace('int c=2*d->pair_slot_o;', 'int c=2*d->pair_slot_o; captured=c+2;')
c=c.replace('void invalidate() {', 'void invalidate() { for(int c=captured;c<64;++c) {expected[c]=0; for(auto& q:expected_wire) if(!q.empty()) q.back()[c]=0;}')
c=c.replace('expected_wire.clear(); wire.clear();','for(auto& q:expected_wire) q.clear(); wire.clear();')
c=c.replace('for(int c=0;c<8;++c) output(c,c%2);','for(int c=0;c<64;++c) output(c,c);')
(out/'sim_main.cpp').write_text(c)
rtl=a.source/'hdl'; f=rtl/'ieee1722/aaf'; av=rtl/'ieee1722/avtp'
src=[rtl/'common/ethernet_packet_pkg.sv',av/'avtp_subtype_pkg.sv',f/'KL_aaf_packetizer.sv',av/'avtp_stream_parser.sv',av/'KL_avtp_rx_monitor.sv',f/'KL_aaf_rx_depacketizer.sv',f/'KL_render_queue.sv',f/'KL_chan_map_capture.sv',a.source/'third_party/verilog-axis/rtl/axis_fifo.v',out/'loopback_wrap.sv',out/'sim_main.cpp']
cmd=[a.simulator,'--cc','--exe','--build','-j','4','--top-module','loopback_wrap','--Mdir',str(out/'obj'),'-Wno-fatal','-Wno-PINMISSING','-Wno-WIDTHEXPAND','-Wno-WIDTHTRUNC','-CFLAGS','-std=c++17 -O2 -DNSTREAMS=8 -DFIRST=1 -DCHANNELS=63 -DLEAD=1']+['+incdir+'+str(p) for p in [rtl/'common',av,f]]+list(map(str,src))+['-o','full_width']
with (out/'build.raw.log').open('w') as log: r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=550)
if r.returncode: print('BUILD FAIL'); raise SystemExit(r.returncode)
with (out/'run.log').open('w') as log: r=subprocess.run([str(out/'obj/full_width')],stdout=log,stderr=subprocess.STDOUT,timeout=120)
(out/'rc').write_text(str(r.returncode)+'\n'); print((out/'run.log').read_text()); raise SystemExit(r.returncode)
