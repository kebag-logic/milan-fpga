"""Run every check of one shape and record the longest service call per flash
port, split into runs where a command-master stall took effect and runs
where none did (the split the lane's own Bench.call_max uses). Usage:
probe_port_maxima.py <repo> <workdir> <config-stem>"""
import sys
from pathlib import Path
repo, work, stem = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_bench  # noqa: E402
import test_ctrl_nvm as T  # noqa: E402
seen: dict = {}
orig = nvm_bench.Bench.run


def run(self, *args):
    r = orig(self, *args)
    port = "litespi" if args and args[0] == "--litespi" else "model"
    kind = "stalled" if r.s.get("ls_stalled") else "nominal"
    key = (port, kind)
    seen[key] = max(seen.get(key, 0), r.s.get("max_call_us", 0))
    return r


nvm_bench.Bench.run = run
inputs = nvm_bench.shape_inputs(repo / "configs" / f"{stem}.yaml", work / "in")
b = T.bench_for(inputs, work)
res = T.grade(b, list(T.CHECKS))
bad = sum(1 for v in res.values() if v)
for (port, kind), v in sorted(seen.items()):
    print(f"{stem} {port:8s} {kind:8s} longest_call_us={v}")
print(f"{stem} failed_checks={bad}")
