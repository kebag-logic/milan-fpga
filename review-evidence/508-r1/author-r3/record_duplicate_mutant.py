"""Record the duplicated-withdrawal mutant's raw G8 failures at the final head.

Uses the committed campaign's plant/build/run functions, with copies only.
Run from the candidate worktree. The temporary processor copy is removed.
"""
import importlib.util
from pathlib import Path
import tempfile

out = Path(__file__).resolve().parent
script = Path("tb/verilator/milan_dp/gsi_mutants.py").resolve()
spec = importlib.util.spec_from_file_location("gsi_mutants", script)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
mutation = gate.MUTATIONS[-1]
assert "duplicates the withdrawal" in mutation[0]
with tempfile.TemporaryDirectory(prefix="508-a297-duplicate-") as temp:
    work = Path(temp)
    dp, pp = gate.plant(mutation[0], mutation[1], work, "withdrawal")
    exe = gate.build(dp, pp, work / "obj_duplicate")
    assert exe is not None
    rc, log = gate.run_leg(exe)
    (out / "duplicate-mutant-raw.log").write_text(log)
    assert gate.verdict(rc, log, mutation[2]) == "caught"
    for controller in ["A", "B"]:
        check = "[GSI] G8 sink 0 withdrawn: unsolicited GET_STREAM_INFO(sink 0) to " + controller
        failed = [line for line in log.splitlines() if line.strip().startswith("[FAIL]") and check in line]
        assert len(failed) == 1, (controller, failed)
        assert "got=0x3 exp=0x2" in failed[0], failed[0]
        print(failed[0])
    print("PASS: both named G8 counts reject three pushes instead of two; mutant exit", rc)
