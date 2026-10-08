import hashlib,importlib.util,json,os,re,shutil,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
root=w/"functional/route"
common=w/"timing/ax7101/gateware"
big=w/"timing/ax8x8/gateware"
vendor=str(Path.home()/"Xilinx/2026.1/Vivado/bin/vivado")
rows=[]
def run(name,argv,cwd,env=None,required=True):
 spec=dict(argv=argv,cwd=str(cwd),env=env or {})
 (w/"jobs"/(name+".json")).write_text(json.dumps(spec))
 with (w/"logs"/(name+".launcher.log")).open("w") as f:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"vendor_job.py"),name],stdout=f,stderr=subprocess.STDOUT)
  (w/"jobs"/(name+".pid")).write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True);rc=p.wait()
 print(time.strftime("%FT%T"),"DONE",name,rc,flush=True)
 rows.append(dict(name=name,rc=rc));(w/"vendor-results.json").write_text(json.dumps(rows,indent=2)+"\n")
 if required and rc:raise SystemExit(rc)
 return rc
def execute(name,script,cwd,env=None,required=True):
 return run(name,["flock","$VIVADO_LOCK",vendor,"-mode","batch","-source",script,"-nojournal","-log",name+".vendor.log"],cwd,env,required)
# Admission is explicit: the caller starts this bank after all build jobs finish.
for marker in ("functional-complete","sweeps-complete","extra-complete","litex-complete","firmware-campaigns-complete"):
 assert (w/marker).exists(),marker
for name in ("sweep-0-rerun","sweep-1-rerun","builder","physical","portability","arrival","quiet-reader","follow-pullin","render-default","dev-render-default","render-pullin","render-boundary","fw-ctrl","fw-nvm","fw-coverage","bdd-tests","litex-controls","litex-sims","fw-mutants","fw-image","fw-image-controls"):
 assert (w/"logs"/(name+".rc")).read_text().strip()=="0",name
# Resource comparison retains the baseline recipe's identity script in full.
source=(common/"baseline_integrated.tcl").read_text()
assert source.count("# Add pre-optimize commands")==1
prefix,tail=source.split("# Add pre-optimize commands")
(common/"synthesis_only.tcl").write_text(prefix+"\nquit\n")
assert tail.rstrip().endswith("quit")
tail=tail.rstrip()[:-4]+"write_bitstream -force alinx_ax7101.bit\nquit\n"
run("vendor-parser",["flock","$VIVADO_LOCK","python3","-B","scripts/xvlog_gate.py","--check"],Path("$REPO"))
execute("shipping-synthesis","synthesis_only.tcl",common)
spec=importlib.util.spec_from_file_location("constraints",root/"sw/litex/clock_constraints.py")
constraints=importlib.util.module_from_spec(spec);spec.loader.exec_module(constraints)
for directive in ("ExtraPostPlacementOpt","AltSpreadLogic_high","ExtraTimingOpt"):
 build=common.parent if directive=="ExtraPostPlacementOpt" else w/"timing"/("ax7101-"+directive)
 gate=build/"gateware";gate.mkdir(parents=True,exist_ok=True)
 script="set_param general.maxThreads 32\nopen_checkpoint {"+str(common/"alinx_ax7101_synth.dcp")+"}\n# Add pre-optimize commands"+tail
 script=script.replace("place_design -directive ExtraPostPlacementOpt","place_design -directive "+directive)
 (gate/"implementation.tcl").write_text(script)
 for relative in ("software/include/generated/soc.h","aem_desc.bin"):
  if build!=common.parent:
   dst=build/relative;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(common.parent/relative,dst)
 rc=execute(directive+"-implementation","implementation.tcl",gate,required=False)
 if rc:continue
 combined=gate/"vivado.log"
 combined.write_text((common/"shipping-synthesis.vendor.log").read_text()+"\n"+(gate/(directive+"-implementation.vendor.log")).read_text())
 try:constraints.check_implementation_log(combined)
 except BaseException as err:
  for p in gate.glob("*.bit"):p.rename(p.with_suffix(".bit.rejected"))
  (w/"logs"/(directive+"-constraint-check.rc")).write_text("1\n")
  (w/"logs"/(directive+"-constraint-check.log")).write_text(str(err)+"\n")
  continue
 (w/"logs"/(directive+"-constraint-check.rc")).write_text("0\n")
 run(directive+"-manifest",["python3","-B",str(root/"sw/litex/layout_from_soch.py"),str(build),"--bit",str(gate/"alinx_ax7101.bit")],root)
# All rows are available before the manual best-image grade.
(w/"timing-complete").write_text("complete\n")
run("timing-grade",["python3","-B",str(w/"grade_vendor.py")],w)
# Route endpoint is the recorded placement recipe, even if another image is kept.
run("resource-route-1x1",["python3","-B","syn/ooc/pp_resource_gate.py","check",str(common),"--endpoint","route-1x1"],root)
execute("integrated-8x8-synthesis","baseline_integrated.tcl",big)
for shape,gate,log in (("1x1",common,common/"shipping-synthesis.vendor.log"),("8x8",big,big/"integrated-8x8-synthesis.vendor.log")):
 out=w/"timing"/("ooc-"+shape)
 run("prepare-ooc-"+shape,["python3","-B","syn/ooc/pp_baseline.py",str(gate),"--output",str(out),"--integrated-log",str(log),"--integrated-clock","--single-thread-synthesis"],root)
 execute("ooc-"+shape,"baseline_ooc.tcl",out)
 run("resource-ooc-"+shape,["python3","-B","syn/ooc/pp_resource_gate.py","check",str(out),"--endpoint","ooc-"+shape],root)
for shape in ("settle_base","settle_head","cmc_base","cmc_head"):
 execute("own-"+shape,"ooc.tcl",w/"area-ooc",env={"ONLY":shape})
run("own-area-grade",["python3","-B",str(w/"grade_area.py")],w)
run("gmii-placement",["flock","$VIVADO_LOCK",vendor,"-mode","batch","-nojournal","-log","gmii-placement.vendor.log","-source",str(root/"sw/litex/gmii_rx_capture_check.tcl"),"-tclargs",str(w/"gmii-fixtures")],w/"gmii-fixtures")
(w/"vendor-complete").write_text("complete\n")
(w/"vendor.rc").write_text("0\n")
