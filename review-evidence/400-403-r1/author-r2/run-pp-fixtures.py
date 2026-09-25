import json, shlex, subprocess, sys
from pathlib import Path
p=Path(__file__).resolve().parent
root=Path("$LANES/400-403-declaration-truth")
cwd=root/"tb/verilator/pp_shadow"
for name,defs in (("vid73","-DDECLARATION_VID=73"),("crf-on","-DDECLARATION_OUTPUTS=2")):
 mdir="obj_decl_"+name.replace("-","_")
 fixture="$VALIDATION_STORAGE/400-403-a313-tools/fixtures/"+name
 sources=subprocess.run(["make","--no-print-directory","-s","-C","../milan_dp","print-srcs"],cwd=cwd,capture_output=True,text=True,check=True).stdout.strip()
 cmd=["make","--no-print-directory","-n","run","VERILATOR=$VALIDATION_STORAGE/400-403-a313-tools/bin/verilator", "SHAPE_1x1=+incdir+"+fixture,"TIM_D=-DPP_MS_CYCLES=100 "+defs,"DP_SRCS="+sources]
 plan=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,check=True).stdout
 (p/("pp-"+name+"-plan.txt")).write_text(plan)
 for command in plan.replace("\\\n"," ").splitlines():
  if not command or command.startswith("#"): continue
  args=shlex.split(command)
  if args[0].endswith("/verilator"):args[1:1]=["--Mdir",mdir]
  if args[0]=="./obj_dir/Vpp_shadow_sim":args[0]="./"+mdir+"/Vpp_shadow_sim"
  print("COMMAND",repr(args),flush=True)
  subprocess.run(args,cwd=cwd,check=True,timeout=14400)
