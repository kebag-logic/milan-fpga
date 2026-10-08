import subprocess,sys,tarfile
from pathlib import Path
r=Path(__file__).resolve().parent
commands=[("em-dash-final",["python3","scripts/check_em_dash.py","--base","d8b355fe0f41d49dca6cae1cd8b3826e2edde364"]),
 ("docs-final",["python3","scripts/docs_check.py"]),
 ("docs-wire",["python3","scripts/check_wire_accountability.py","--self-test"]),
 ("cpp-final",["python3","scripts/check_cpp_idiom.py"]),
 ("py-final",["python3","scripts/check_py_idiom.py"]),
 ("toc-final",["python3","scripts/gen_toc.py","--check"]),
 ("doc-paths-final",["python3","scripts/check_doc_paths.py"]),
 ("doc-style-final",["python3","scripts/check_doc_style.py"]),
 ("source-diff",["git","diff","--check","82a79638405c3365e4078da471be56758f8dd679","HEAD"])]
for label,command in commands:
 subprocess.run([sys.executable,str(r/"run.py"),label,*command],check=True,timeout=550)
a=r/"committed-source.tar"; dest=r/"committed-source"; dest.mkdir(exist_ok=True)
subprocess.run(["git","archive","--format=tar","--output",str(a),"HEAD"],check=True)
with tarfile.open(a) as f: f.extractall(dest,filter="data")
for label,command in [("docs-archive",["python3","scripts/docs_check.py"]),
 ("docs-archive-feature",["python3","scripts/check_feature_status.py"])]:
 subprocess.run([sys.executable,str(r/"run.py"),label,*command],cwd=dest,check=True,timeout=550)
