import sys,json,shutil
from pathlib import Path
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import build
build.JOBS=4
out=Path(sys.argv[1]); variant=sys.argv[2]
assert shutil.disk_usage(out.parent).free>=20_000_000_000
spec=build.build(out,'endstation_arty_current',1,variant=variant)
(out/'build.json').write_text(json.dumps(spec,indent=2)+'\n')
build.reused(out)
