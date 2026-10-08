import subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
label=sys.argv[1]
with (r/(label+".driver.log")).open("w") as log:
 p=subprocess.Popen(["setsid","nohup",sys.executable,str(r/"run.py"),*sys.argv[1:]],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
(r/(label+".pid")).write_text(str(p.pid)+"\n")
print(label,p.pid)
