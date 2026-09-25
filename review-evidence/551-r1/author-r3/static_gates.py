import os, subprocess, sys
from pathlib import Path
out=Path(__file__).resolve().parent
root=Path.cwd()
gates=[
("behave",["behave","--no-capture","-f","plain"],root/"tests"),
("docs_git",["python3","scripts/docs_check.py"],root),
("docs_no_git",["env","GIT_DIR=/tmp/551-a312-no-git-absent","python3","scripts/docs_check.py"],root),
("em_dash",["python3","scripts/check_em_dash.py","--base","864b36f5e9450ef64f75ca3f0d68c44330e447d7"],root),
("doc_style",["python3","scripts/check_doc_style.py"],root),
("gen_toc",["python3","scripts/gen_toc.py","--check"],root),
("doc_paths",["python3","scripts/check_doc_paths.py"],root),
("module_matrix",["python3","docs/traceability/gen_module_matrix.py","--check"],root),
("xvlog",["python3","scripts/xvlog_gate.py","--check"],root),
("rtl_source_lists",["python3","scripts/check_rtl_source_lists.py"],root),
("py_idiom",["python3","scripts/check_py_idiom.py"],root),
("cpp_idiom",["python3","scripts/check_cpp_idiom.py"],root),
("diff_check",["git","diff","--check"],root),
]
failures=[]
for name,cmd,cwd in gates:
 rc=subprocess.run([sys.executable,str(out/"run_gate.py"),name,*cmd],cwd=cwd,timeout=14460).returncode
 if rc: failures.append(name)
print("Failed gates:",failures,flush=True)
sys.exit(bool(failures))
