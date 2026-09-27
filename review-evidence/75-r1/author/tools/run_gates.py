"""Run the assigned gates without pipelines and retain exact return codes."""
from pathlib import Path
import subprocess,json,sys
p=Path(__file__).resolve().parent.parent
repo=Path("$LANES/75-reconnect-bench")
py=sys.executable
cmds=[[py,"-B","scripts/docs_check.py"],[py,"-B","scripts/check_doc_style.py"],[py,"-B","scripts/gen_toc.py","--check"],[py,"-B","scripts/check_em_dash.py","--base","8bc97021"],[py,"-B","scripts/check_doc_paths.py"],[py,"-B","scripts/ci_scope.py","--selftest"],["python3","-B","scripts/check_baremetal_only.py","--check"],[py,"-B","scripts/check_feature_status.py","--self-test"],["git","diff","--check"]]
results=[]
for n,cmd in enumerate(cmds,1):
 actual=["rtk","proxy","timeout","90s",*cmd]
 r=subprocess.run(actual,cwd=repo,capture_output=True,text=True,timeout=95)
 text="COMMAND "+" ".join(actual)+"\nCWD "+str(repo)+"\n"+r.stdout+r.stderr+"\nRC "+str(r.returncode)+"\n"
 assert len(text.encode())<=200000
 (p/f"gate-{n}.txt").write_text(text)
 results.append(dict(command=actual,rc=r.returncode))
 print(f"gate {n}: rc {r.returncode}",flush=True)
(p/'gates.json').write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(r['rc'] for r in results))
