# SPDX-License-Identifier: Apache-2.0
import shutil
from common import *
src=SCRATCH/"embedded-source"
for name in ("src","tests"):
 shutil.copytree(SOURCE/name,src/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__"))
shutil.copy2(SOURCE/"CMakeLists.txt",src)
f=src/"tests/check_embedded.py"
f.write_text(f.read_text().replace("\"--parallel\", \"2\"","\"--parallel\", \"16\""))
run("embedded-boundary",["python3",f,"--work-dir",SCRATCH/"embedded-build"],cwd=src)
