import subprocess,sys
from pathlib import Path
w=Path(sys.argv[1])
for variant in sys.argv[2:]:
 shape="8" if variant.endswith("@8") else "1"
 name=variant.split("@")[0]
 cmd=[sys.executable,"tb/verilator/milan_dp/stream_counters.py","--shape",shape,"--variant",name,"--work",str(w/("stream-"+variant))]
 print("RUN",variant,flush=True)
 subprocess.run(cmd,check=True)
 print("PASS",variant,flush=True)
