"""F1 control: does the engine arm still pass the two #87 mutants when the
harness no longer prints the checks they name?

usage: f1_control.py <repo tree> <label>
The tree's harness is expected to have its "#87 G1 to G2 without a TLV"
checks renamed already. Runs the arm's own unmutated control, then
run_mutant() for the two #87 mutants, so every verdict line printed is the
arm's own wording. Exit 0 always; the verdicts are the evidence.
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
print("tree:", sys.argv[2], flush=True)
spec = importlib.util.spec_from_file_location(
    "arm", tree / "tb/verilator/engine/mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
WANT = ("the empty sequence published without a TLV",
        "a TLV-less Announce publishes {thisClock}")
with tempfile.TemporaryDirectory(prefix="f1-") as td:
    work = Path(td)
    src = m.stage(work, "clean")
    run = work / "run_clean"
    exe = m.build(src, work, "clean")
    assert exe is not None and m.generate_image(src, run)
    print("control:", m.verdict(*m.run_harness(exe, run)), flush=True)
    for mutation in m.MUTATIONS:
        if mutation[0] in WANT:
            print("arm verdict:", m.run_mutant(work, exe, mutation),
                  flush=True)
