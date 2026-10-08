import concurrent.futures as cf,json,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
root=w/"functional/physical"
def run(name,argv):
 (w/"jobs"/(name+".json")).write_text(json.dumps(dict(argv=argv,cwd=str(root))))
 with (w/"logs"/(name+".launcher.log")).open("w") as f:
  p=subprocess.Popen(["setsid","nohup","python3","-B",str(w/"run_job.py"),name],stdout=f,stderr=subprocess.STDOUT)
  (w/"jobs"/(name+".pid")).write_text(str(p.pid)+"\n")
  print(time.strftime("%FT%T"),"START",name,p.pid,flush=True);rc=p.wait()
 print(time.strftime("%FT%T"),"DONE",name,rc,flush=True)
 return rc
def firmware():
 jobs=[("fw-tally",["python3","-B","sw/firmware/gtest/tally_selftest.py"]),
 ("fw-rv32",["python3","-B","sw/firmware/gtest/fw_rv32_selftest.py","--require-rv32"]),
 ("fw-ctrl",["python3","-B","sw/firmware/ctrl/test/test_ctrl_firmware.py","--require-rv32","--jobs","4"]),
 ("fw-nvm",["python3","-B","sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py","--require-rv32","--jobs","4"]),
 ("fw-coverage-selftest",["python3","-B","sw/firmware/gtest/fw_coverage.py","--selftest"]),
 ("fw-coverage",["python3","-B","sw/firmware/gtest/fw_coverage.py","--check","--jobs","4"])]
 for name,argv in jobs:run(name,argv)
def fast():
 jobs=[("bdd",["$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/behave","--no-capture","-f","plain"]),
 ("source-controls",["python3","-B","scripts/check_rtl_source_lists.py","--selftest"]),
 ("wire-controls",["python3","-B","tb/tools/avtp_wire_truth.py","--self-test"]),
 ("baseline-selftest",["python3","-B","syn/ooc/pp_baseline.py","--selftest"]),
 ("resource-selftest",["python3","-B","syn/ooc/pp_resource_gate.py","--selftest"]),
 ("resource-baseline",["python3","-B","syn/ooc/pp_resource_gate.py","check-baseline"]),
 ("gmii-capture",[str(Path.home()/"litex-milan/venv/bin/python3"),"-B","sw/litex/test_gmii_rx_capture.py","--emit-dir",str(w/"gmii-fixtures")])]
 for name,argv in jobs:run(name,argv)
with cf.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(f) for f in (firmware,fast)]
 for f in cf.as_completed(fs):f.result()
(w/"extra-complete").write_text("complete\n")
