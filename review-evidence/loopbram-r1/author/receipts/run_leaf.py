import os,sys,subprocess,json,time
from pathlib import Path
root=Path('$CHECKOUT');w=Path('$SCRATCH/leaf');w.mkdir(exist_ok=True)
for enabled in [0,1]:
 d=w/str(enabled);d.mkdir(exist_ok=True)
 tcl=d/'leaf.tcl';tcl.write_text(f"""set_param general.maxThreads 8
read_verilog -sv {root}/hdl/ieee1722/aaf/KL_render_queue.sv
synth_design -mode out_of_context -top KL_render_queue -part xc7a100t-fgg484-2 -directive AreaOptimized_high -generic INPUT_LOOPBACK_P={enabled} -generic CLK_FREQ_HZ_P=50000000 -generic IF_LEAD_P=1
create_clock -period 20 [get_ports clk_i]
opt_design -directive ExploreArea
report_utilization -hierarchical -file leaf_hier.rpt
report_utilization -file leaf_util.rpt
write_checkpoint -force leaf.dcp
quit
""")
 cmd=['<home-path>/milan-fpga-management/2026-09-23/vivado-slot.sh','<home-path>/Xilinx2/2026.1/Vivado/bin/vivado','-mode','batch','-nojournal','-nolog','-source',str(tcl)]
 start=time.time()
 with (d/'leaf.log').open('w') as log:r=subprocess.run(cmd,cwd=d,env=dict(os.environ,VIVADO_SLOTS='2',VIVADO_MIN_GB='20'),stdout=log,stderr=subprocess.STDOUT,timeout=14400)
 (d/'result.json').write_text(json.dumps({'command':cmd,'exit':r.returncode,'seconds':time.time()-start},indent=2));print('LEAF',enabled,r.returncode,flush=True)
 if r.returncode:sys.exit(r.returncode)
