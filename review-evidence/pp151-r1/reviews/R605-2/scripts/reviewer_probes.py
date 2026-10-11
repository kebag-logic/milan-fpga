#!/usr/bin/env python3
"""Independent fault probes and a scoped Python-contract audit; no checkout writes."""
import argparse, ast, concurrent.futures, json, os, shutil, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);ap.add_argument("packet",type=Path);ap.add_argument("--verilator",required=True);ap.add_argument("--jobs",type=int,default=4);a=ap.parse_args();r=a.root.resolve();p=a.packet.resolve()
env=dict(os.environ,TMPDIR=str(p/"scratch"),PYTHONDONTWRITEBYTECODE="1",VERILATOR=a.verilator)
# Independent literal defect descriptions; not imported from the campaign under review.
probes=[
("size-23", "hdl/aecp/KL_aecp_resp_buf.sv","RESP_BYTES_P <= 16","RESP_BYTES_P <= 23","KL_aecp_resp_buf.gen_g_size","RESP_BYTES_P=17"),
("shadow-timeout-2","hdl/acmp/KL_acmp_nvm_shadow.sv","RS_TMO_CYC_P < 1","RS_TMO_CYC_P < 2","KL_acmp_nvm_shadow.g_rs_tmo_check","RS_TMO_CYC_P=1"),
("writer-timeout-2","hdl/aecp/KL_aecp_nvm_writer.sv","RS_TMO_CYC_P < 1","RS_TMO_CYC_P < 2","KL_aecp_nvm_writer.g_rs_tmo_check","RS_TMO_CYC_P=1"),
("writer-aggregate-2","hdl/aecp/KL_aecp_nvm_writer.sv","RS_AGG_CYC_P < 1","RS_AGG_CYC_P < 2","KL_aecp_nvm_writer.g_rs_agg_check","RS_AGG_CYC_P=1")]
(p/"receipts/reviewer-probes").mkdir(exist_ok=True)
def run(probe):
 name,path,old,new,guard,value=probe;tree=p/"scratch"/("reviewer-"+name);
 if tree.exists():shutil.rmtree(tree)
 shutil.copytree(r/"hdl",tree/"hdl")
 file=tree/path;source=file.read_text();assert source.count(old)==1;file.write_text(source.replace(old,new))
 cmd=["python3","-B",str(r/"tb/elab_guards/guards.py"),"--root",str(tree),"--frontend","verilator","--verilator",a.verilator,"--jobs","1","--only",guard]
 result=subprocess.run(cmd,cwd=r,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (p/f"receipts/reviewer-probes/{name}.log").write_text(result.stdout)
 (p/f"receipts/reviewer-probes/{name}.rc").write_text(str(result.returncode)+"\n")
 assert result.returncode==1
 assert any(x.startswith("FAIL: ELAB ") and guard in x and value in x and "USERFATAL" in x for x in result.stdout.splitlines()),result.stdout
 return {"probe":name,"result":"KILLED by named passing-case failure", "rc":result.returncode}
with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:results=list(pool.map(run,probes))
# Verify the specific zero-debt obligations in the manager's Round 2 Python ruling.
functions=[]
for rel in ["tb/elab_guards/guards.py","tb/elab_guards/mutants.py"]:
 source=(r/rel).read_text();tree=ast.parse(source)
 for node in ast.walk(tree):
  if not isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) or node.name.startswith("_"):continue
  args=node.args.posonlyargs+node.args.args+node.args.kwonlyargs
  if node.args.vararg:args.append(node.args.vararg)
  if node.args.kwarg:args.append(node.args.kwarg)
  complete=node.returns is not None and all(x.arg in ("self","cls") or x.annotation is not None for x in args)
  documented=bool(ast.get_docstring(node));assert complete and documented,(rel,node.name)
  functions.append({"path":rel,"function":node.name,"line":node.lineno,"signature":complete,"docstring":documented})
(p/"receipts/python-contract-audit.json").write_text(json.dumps(functions,indent=2)+"\n")
print(json.dumps({"fault_probes":results,"annotated_documented_functions":len(functions)},indent=2))
