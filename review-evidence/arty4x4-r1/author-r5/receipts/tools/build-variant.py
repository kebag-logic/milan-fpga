"""One census image at the Arty 4x4 point. usage: build-variant.py <dir> <variant>"""
import sys, json, shutil
from pathlib import Path
ROOT = Path('$LANES/arty-4x4')
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import build
build.JOBS = 4
out = Path(sys.argv[1]); variant = sys.argv[2]
assert shutil.disk_usage(out.parent).free >= 15_000_000_000
spec = build.build(out, 'endstation_arty_split_4x4', 1, variant=variant)
(out / 'build.json').write_text(json.dumps(spec, indent=2) + '\n')
build.reused(out)
print('BUILT', variant, spec['executable_sha256'], spec['cpu_hz'], spec['sys_hz'], flush=True)
