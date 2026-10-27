"""S1: whether the coverage rule can see control #295 (a returned excursion's bit-flip left for the hold).

Applies that control to a temporary planner copy and, for R699-6's minimal case (0x80100 over channel 0's
words 4424 to 6149, a DUT repeat of 3 at 6097 on every channel), prints channel 0's DUT listings and the
gate's _fuzz_check result, pristine and mutated; then runs the gate test and the pin on the mutated copy.

usage: python3 -I -B s1_fuzz_vs_295.py <tb/tools dir>
"""
import subprocess
import sys
import tempfile
from pathlib import Path

tools = Path(sys.argv[1])
sys.path.insert(0, str(tools))
from torture_release_audio_mutants import AUDIO_GRADER_MUTANTS  # noqa: E402

name, old, new, pin = next(m for m in AUDIO_GRADER_MUTANTS if m[0].startswith("a returned excursion's bit-flip"))
PROBE = """
import sys, unittest
sys.path.insert(0, sys.argv[1])
import torture_campaign as t
class T(t._ReleaseGateChecks, unittest.TestCase):
    def runTest(self):
        pass
c = T()
run = [{"kind": "flip", "index": 4424 + k, "channel": 0, "mask": 0x80100} for k in range(1726)]
units = [("run", 4424, [0], 1726, run), ("slip", 6097, [0, 1, 2, 3], 1, [{"kind": "repeat", "index": 6097, "n": 3}])]
verdict, detail, _ = c._sweep_grade(16384, run + units[1][4])
print("channel 0:", [(e["capture_index"], e["class"], e["n"]) for e in detail["events"]
                     if e["attribution"] == "dut" and e["channel"] == 0])
print("_fuzz_check:", c._fuzz_check(16384, units))
for test in sys.argv[2:]:
    r = unittest.TestResult()
    T(test).run(r)
    print(test, "FAIL" if r.failures or r.errors else "ok")
"""
text = (tools / "torture_campaign.py").read_text(encoding="utf-8")
assert text.count(old) == 1
print("control:", name)
for label, body in (("pristine", text), ("mutated", text.replace(old, new))):
    with tempfile.TemporaryDirectory(prefix="r8-s1-") as directory:
        (Path(directory) / "torture_campaign.py").write_text(body, encoding="utf-8")
        tests = ["test_audio_compositions_never_pass_and_list_every_event", pin]
        run = subprocess.run([sys.executable, "-I", "-B", "-c", PROBE, directory, *tests],
                             capture_output=True, text=True, timeout=900)
        print(f"[{label}] rc={run.returncode}")
        print(run.stdout.strip() or run.stderr.strip()[-400:])
