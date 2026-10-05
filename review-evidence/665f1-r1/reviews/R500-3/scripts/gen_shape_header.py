"""Write the suite's nvm_shape_gen.h for one config into <work>/gen, using the
lane's own derivation (sw/firmware/ctrl_nvm/test/nvm_bench.py)."""
import sys
from pathlib import Path
repo, cfg, work = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_bench  # noqa: E402
inputs = nvm_bench.shape_inputs(repo / "configs" / f"{cfg}.yaml", work / "b")
(work / "gen").mkdir(parents=True, exist_ok=True)
(work / "gen" / "nvm_shape_gen.h").write_text(
    nvm_bench.shape_header(inputs.shape, inputs.donor, inputs.ident))
print("wrote", work / "gen" / "nvm_shape_gen.h")
