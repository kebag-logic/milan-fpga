"""Build and run against a supplied processor checkout; all builds stay in scratch.
Usage: python3 run_reproduction.py PROCESSOR_CHECKOUT BUILD_DIRECTORY
"""
from pathlib import Path
import subprocess
import sys
if sys.flags.optimize:
    raise SystemExit("optimized execution unsupported")
pp, build = [Path(p).resolve() for p in sys.argv[1:3]]
deferred=len(sys.argv)>3 and sys.argv[3]=="deferred"
out=Path(__file__).resolve().parent
build.mkdir(parents=True,exist_ok=True)
wrapper=(pp/'tb/srp_top/srp_top_wrap.sv').read_text()
wrapper=wrapper.replace('    input  wire         clk_i,', '    output wire [15:0] probe_reg_o,\n    output wire [31:0] probe_la_deadline_o,\n    input  wire         clk_i,',1)
wrapper=wrapper.replace('  // Read-only probes:', '  assign probe_reg_o = u_dut.u_talker.dbg_reg_state_o;\n  assign probe_la_deadline_o = u_dut.cad_dl_r[3];\n\n  // Read-only probes:',1)
(build/'srp_top_wrap.sv').write_text(wrapper)
files=['common/pp_pkg.sv','srp/srp_pkg.sv','common/KL_pp_prng.sv','common/KL_pp_timer_service.sv','packet_engine/KL_pp_tx_slots.sv']
files += ['srp/KL_srp_'+s+'.sv' for s in ['decoder','domain','vlan','talker_fsm','listener_fsm','admission','encoder','top']]
cmd=['verilator','--cc','--exe','--build','-j','4','--top-module','srp_top_wrap','-Wno-fatal','--Mdir',str(build/'obj'),'-CFLAGS',f'-std=c++17 -O2 -I{pp}/tb']
paths=[str(pp/'hdl'/p) for p in files]
if deferred:
    original=pp/'hdl/srp/KL_srp_talker_fsm.sv'
    source=original.read_text()
    old='leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;'
    if source.count(old)!=1: raise SystemExit('counterfactual target mismatch')
    source=source.replace(old,'leaveall_rx_i[SRP_LA_LISTENER_C] || (join_tick_i && laown_pend_r);')
    variant=build/'KL_srp_talker_fsm.sv';variant.write_text(source)
    paths[paths.index(str(original))]=str(variant)
cmd += paths+[str(build/'srp_top_wrap.sv'),str(out/'reproduce.cpp'),'-o','reproduce']
with (build/'build.log').open('w') as log:
    r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=600)
if r.returncode:
    print((build/'build.log').read_text()[-7000:]);raise SystemExit(r.returncode)
r=subprocess.run([str(build/'obj/reproduce')]+(['deferred'] if deferred else []),capture_output=True,text=True,timeout=180)
print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr)
(out/('simulation-counterfactual.txt' if deferred else 'simulation-results.txt')).write_text(r.stdout+r.stderr)
raise SystemExit(r.returncode)
