"""Plant one named defect from the lane's own table and print EVERY finding
the named checks report (the self-test prints only the first). Usage:
probe_mutant_findings.py <repo> <workdir> <mutant> [config-stem]"""
import sys
from pathlib import Path
repo, work, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
stem = sys.argv[4] if len(sys.argv) > 4 else "endstation_ax7101_1x1_tdm8"
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_bench  # noqa: E402
import nvm_mutants  # noqa: E402
import test_ctrl_nvm as T  # noqa: E402
m = next(x for x in nvm_mutants.MUTANTS if x.name == name)
tree = work / name / "tree"
nvm_mutants.plant(m, tree)
inputs = nvm_bench.shape_inputs(repo / "configs" / f"{stem}.yaml", work / "in")
b = T.bench_for(inputs, work / name, tree)
res = T.grade(b, list(m.kills))
for k, v in res.items():
    print(f"{name} / {k}: {len(v)} finding(s)")
    for x in v:
        print("   ", x[:260])
