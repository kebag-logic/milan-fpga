# Standalone validation helper; run from a candidate checkout.
import os
from pathlib import Path
import sys
repo = Path.cwd()
work = Path(os.environ["VALIDATION_WORK"]).resolve() / "asan-witness"
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as gate
m = next(m for m in gate.nvm_mutants.MUTANTS if m.name == "erased_payload_end_bound")
shape = gate.prepare(gate.ROOT / "configs" / f"{gate.SELF_TEST_SHAPE}.yaml", work / "shape")
tree = work / "tree"
gate.nvm_mutants.plant(m, tree)
exes = gate.build(shape, work / "build", gate.fw_gtest.Build(jobs=4), tree)
held = gate.suite_tests(exes, shape)
log = ""
for binary in gate.binaries(shape):
    kills = [k for k in m.kills if held.get(k) == binary.name]
    if kills:
        log += gate.run_suite(exes[binary.name], gate.fixture_of(shape, binary), kills)[1]
print(log)
assert "AddressSanitizer: heap-buffer-overflow" in log
assert "[FAIL] NvmCodec.codec_erased_loaded_prefix" in log
print("witness: restored end bound reads past the exact-sized loaded buffer; named test fails")
