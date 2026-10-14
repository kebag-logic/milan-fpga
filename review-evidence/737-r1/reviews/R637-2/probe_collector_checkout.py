#!/usr/bin/env python3
"""Reproduce collector inventory reads in a checkout without submodules."""
import io,json,os,pathlib,subprocess,sys,tarfile
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parent
checkout=packet/"scratch"/"collector-checkout"; checkout.mkdir(parents=True,exist_ok=True)
archive=subprocess.check_output(["git","archive","HEAD","scripts","tb","hdl","configs"],cwd=root)
with tarfile.open(fileobj=io.BytesIO(archive)) as stream: stream.extractall(checkout,filter="data")
# An ordinary actions/checkout creates gitlink directories without their contents.
links=subprocess.check_output(["git","ls-tree","-r","HEAD"],cwd=root,text=True)
for line in links.splitlines():
 if line.startswith("160000 "): (checkout/line.split("\t",1)[1]).mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(checkout/"scripts"))
from ci_runtime_evidence import suite_evidence
from ci_suite_pieces import inventory
from ci_gate_workflows import generate,load_template
workflow=generate("rtl",load_template(root,"rtl"))
steps=workflow["jobs"]["ci-manifest"]["steps"]
print("collector checkout:",json.dumps(steps[0],sort_keys=True))
assert not steps[0].get("with",{}).get("submodules")
assert not any("submodule update" in step.get("run","") for step in steps)
source={"head":"a"*40,"tree":"b"*40}
for suite in ("milan_dp","milan_dp_render","pp_shadow"):
 names=inventory(suite,root)
 artifacts=packet/"scratch"/"collector-input"/suite; artifacts.mkdir(parents=True,exist_ok=True)
 (artifacts/"union.json").write_text(json.dumps({**source,"suite":suite,"inventory":names,
   "legs":[],"union":"pass","verdicts_sha256":"c"*64}))
 try: suite_evidence(source,artifacts)
 except subprocess.CalledProcessError as exc:
  print(suite,"collector inventory failed, rc",exc.returncode)
  print("driver stderr:",exc.stderr.strip().replace(str(checkout),"<checkout>"))
 else: raise AssertionError("collector no longer requires missing submodules")
 child=subprocess.run(["make","-s","--no-print-directory","-C",str(checkout/"tb/verilator"/suite),"ci-list"],capture_output=True,text=True)
 print("Makefile refusal:",child.stderr.strip().replace(str(checkout),"<checkout>"))
 assert child.returncode != 0
print("PASS reproduction: three valid union inventories cannot be collected in the generated checkout.")
