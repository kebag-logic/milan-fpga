#!/usr/bin/env python3
"""Compare the focused read-only traceability gate at base and head."""
import difflib, importlib.util, json, os, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
R=Path(os.environ.get("REVIEW_REPO",str(Path.cwd()))).resolve()
S=P/"scratch/traceability-base"; S.mkdir(exist_ok=True)
archive=P/"scratch/traceability-base.tar"
with archive.open("wb") as f:
 subprocess.run(["git","-C",str(R),"archive","28f9666feab2b2ba287643c63ed3a16b1e0bb863","hdl","tb","docs/traceability"],stdout=f,check=True)
subprocess.run(["tar","-xf",str(archive),"-C",str(S)],check=True)
results={}
for label,root in [("base",S),("head",R)]:
 command=["python3","-B",str(root/"docs/traceability/gen_module_matrix.py"),"--check"]
 r=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (P/"receipts"/("traceability-"+label+".log")).write_bytes(r.stdout)
 (P/"receipts"/("traceability-"+label+".rc")).write_text(str(r.returncode)+"\n")
 results[label]={"rc":r.returncode,"command":command}
 spec=importlib.util.spec_from_file_location("matrix_"+label,root/"docs/traceability/gen_module_matrix.py")
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 rows=m.build();artifacts={m.TRACE/"MODULE_MATRIX.md":m.render_top(rows)};artifacts.update(m.leaf_files(rows))
 diff=[]
 for f,content in artifacts.items():
  old=f.read_text() if f.exists() else ""
  diff.extend(difflib.unified_diff(old.splitlines(True),content.splitlines(True),fromfile=str(f.relative_to(root)),tofile=str(f.relative_to(root))+" (regenerated)"))
 (P/"receipts"/("traceability-"+label+".diff")).write_text("".join(diff))
print(json.dumps(results,indent=2))
