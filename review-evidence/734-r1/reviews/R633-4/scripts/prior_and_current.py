#!/usr/bin/env python3
"""Rerun original probes unchanged, then grade their observations at the current head."""
import contextlib,importlib.util,io,json,pathlib,subprocess,sys
mode=sys.argv[1]; source=pathlib.Path("/work");work=pathlib.Path("/tmp")
def run(args):
 r=subprocess.run(args,text=True,capture_output=True);print("COMMAND",args,"rc",r.returncode,flush=True);print(r.stdout+r.stderr,flush=True);return r
if mode=="round1":
 r=run(["git","clone","-q","--shared",str(source),"/tmp/copy"]);assert r.returncode==0
 probe="/review/prior/probe_scope.py"
 assert run([sys.executable,probe,"/tmp/copy","/tmp/original"]).returncode==0
 spec=importlib.util.spec_from_file_location("prior",probe);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.PARENT=m.HEAD;m.HEAD=subprocess.check_output(["git","-C",str(source),"rev-parse","HEAD"],text=True).strip()
 sys.argv=[probe,"/tmp/copy","/tmp/current"];capture=io.StringIO()
 with contextlib.redirect_stdout(capture): assert m.main()==0
 print(capture.getvalue()); rows=[json.loads(s) for s in capture.getvalue().splitlines() if s.startswith("{")]
 rows=[r for r in rows if r.get("bodies")=="head"];assert len(rows)==9
 for r in rows:
  assert r["rc"]==0,r
  if r["case"].startswith("B16"):assert r["n"]==2 and r["rtl"]=="false",r
  else:assert r["rtl"]=="true" and "hdl/x.sv" in r["files"],r
 print("PASS: nine current-head observations graded; historical observations retain original oracle")
elif mode=="round2":
 r=run([sys.executable,"-I","/review/prior/probe_r632_2.py",str(source),"/tmp/probe"])
 misses=[s for s in r.stdout.splitlines() if s.startswith("MISS")]
 assert r.returncode==1 and len(misses)==3,(r.returncode,misses)
 for s in misses:assert "identical-on-dev" in s and "hosted=false" in s and "replay=false" in s,s
 print("PASS: only three historical-oracle misses; current requirement is equality on identical-on-dev")
 spec=importlib.util.spec_from_file_location("prior2","/review/prior/probe_r632_2.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 root=pathlib.Path("/tmp/rename-current");root.mkdir();repo=m.Repo(root,source);base=repo.commit(repo.R,{"docs/page.md":"".join(f"line {i}\n" for i in range(40))})
 live=repo.commit(base,{"docs/page.md":None,"docs/reference/REGISTER_MAP.md":"".join(f"line {i}\n" for i in range(40))})
 head=repo.commit(base,{"docs/page.md":"".join(f"line {i}\n" for i in range(40)).replace("line 20","line twenty")})
 for wf,job,sid in m.SCOPES:
  body=m.step_body(source,wf,job,sid);h=m.hosted(repo,body,base,live,head);r=m.replay(repo,body,base,live,head)
  assert h==r==("true",["docs/reference/REGISTER_MAP.md"]),(wf,h,r)
  print("PASS current rename",wf,h,r)
 pathlib.Path("/tmp/old-rename").mkdir()
 assert run(["bash","/review/prior/rename_divergence_r632_2.sh",str(source),"/tmp/old-rename"]).returncode==0
 print("Historical rename script hardcodes old formulas; current actual selectors separately pass above")
elif mode=="external":
 assert run([sys.executable,"/review/prior/scope_audit.py",str(source),"/tmp/audit"]).returncode==0
