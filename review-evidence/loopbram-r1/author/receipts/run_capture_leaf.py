import os,sys,subprocess,json,time
from pathlib import Path
root=Path('$CHECKOUT');w=Path('$SCRATCH/leaf-capture');w.mkdir(exist_ok=True)
for name,legacy,enabled,streams,channels in [('off',0,0,1,2),('mapped',0,1,1,2),('legacy',1,0,8,8)]:
 d=w/name;d.mkdir(exist_ok=True)
 tcl=d/'leaf.tcl';tcl.write_text(f"""set_param general.maxThreads 8
read_verilog -sv {root}/hdl/ieee1722/aaf/KL_chan_map_capture.sv
read_verilog -sv {w}/capture_leaf.sv
synth_design -mode out_of_context -top capture_leaf -part xc7a100t-fgg484-2 -directive AreaOptimized_high -generic INPUT_LOOPBACK_P={enabled} -generic LEGACY_P={legacy} -generic N_LB_STREAMS_P={streams} -generic N_LB_CH_P={channels}
create_clock -period 20 [get_ports clk_i]
opt_design -directive ExploreArea
report_utilization -hierarchical -file leaf_hier.rpt
report_utilization -file leaf_util.rpt
write_checkpoint -force leaf.dcp
quit
""")
 cmd=['<home-path>/milan-fpga-management/2026-09-23/vivado-slot.sh','<home-path>/Xilinx2/2026.1/Vivado/bin/vivado','-mode','batch','-nojournal','-nolog','-source',str(tcl)]
 start=time.time()
 with (d/'leaf.log').open('w') as log:r=subprocess.run(cmd,cwd=d,env=dict(os.environ,VIVADO_SLOTS='2',VIVADO_MIN_GB='20'),stdout=log,stderr=subprocess.STDOUT,timeout=28800)
 (d/'result.json').write_text(json.dumps({'command':cmd,'exit':r.returncode,'seconds':time.time()-start},indent=2));print('CAPTURE LEAF',name,r.returncode,flush=True)
 if r.returncode:sys.exit(r.returncode)
