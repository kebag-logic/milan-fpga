import sys,json
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"tb/verilator/ctrl_service_budget"))
import build
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4')
spec=build.build(r/"arm-fast","endstation_arty_current",1)
assert spec["cpu_hz"]==spec["sys_hz"]==80000000
(r/"arm-fast-prepared.json").write_text(json.dumps(spec,indent=2)+"\n")
print("PREPARED arm-fast",spec["executable_sha256"],flush=True)
