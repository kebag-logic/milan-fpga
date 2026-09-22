import subprocess,tempfile
from pathlib import Path
out=Path(__file__).resolve().parents[1]
source=Path("$VALIDATION_STORAGE/reviews/r225-507-r2")
scratch=Path(tempfile.mkdtemp(prefix="r225-507-r2-"))
(out/"scratch-path.txt").write_text(str(scratch)+"\n")
subprocess.run(["rtk","proxy","git","clone","--quiet","--shared","--no-checkout",str(source),str(scratch/"head")],check=True)
subprocess.run(["rtk","proxy","git","-C",str(scratch/"head"),"checkout","--quiet","--detach","9d6109ccf924c03308cb8aa202ce68a435cd4f8d"],check=True)
(scratch/"old/scripts").mkdir(parents=True)
for name in ("gen_toc.py","gen_toc_cases.py","gen_toc_closer_cases.py","gen_toc_guards.py","check_em_dash.py"):
 data=subprocess.check_output(["rtk","proxy","git","-C",str(source),"show","0d43ff25d38917e77bb5c3d2ddb6473013cea3ba:scripts/"+name])
 (scratch/"old/scripts"/name).write_bytes(data)
print(scratch)
