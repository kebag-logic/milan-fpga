import sys,json
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"tb/verilator/ctrl_split_boot"))
import run
out=Path("$VALIDATION_STORAGE/artysplit-a829/r4/arty-boot")
exe,spec=run.build(out,"endstation_arty_split",1)
(out/"prepared.json").write_text(json.dumps(dict(executable=str(exe),spec=spec),indent=2)+"\n")
print("PREPARED",exe,flush=True)
