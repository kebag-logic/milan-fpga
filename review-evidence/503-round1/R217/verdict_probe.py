import importlib.util
import os
from pathlib import Path
import sys

ev = Path('/data/milan/reviews/r217-scratch/evidence/design-evidence/500-materialization/proposal-evidence')
spec = importlib.util.spec_from_file_location('d3verdict', ev / 'run.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
# A deliberately surviving/no-op mutant: supply the unchanged baseline
# executable under the runner's expected mutant name, in separate scratch.
target = r.OUT / 'build/mut-M01_taint_ignored/obj/d3sim'
target.parent.mkdir(parents=True, exist_ok=True)
os.link('/data/milan/reviews/r217-scratch/d3/build/base-1x1/obj/d3sim', target)
r.HERE = r.OUT
sys.argv = ['run.py', 'run', 'mut-M01_taint_ignored', '--shapes', '1x1', '--pool', '1']
rc = r.main()
print('RUNNER_RETURN', rc)
sys.exit(rc)
