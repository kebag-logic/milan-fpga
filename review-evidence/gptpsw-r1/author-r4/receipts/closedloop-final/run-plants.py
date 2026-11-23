"""Run the existing closed-loop plants after a separately completed full baseline.

Separate foreground units keep each leg within the execution window. No plant,
test, expected failing word, or pass condition is changed.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
from pathlib import Path
import subprocess
import sys

repo, work, baseline = map(Path, sys.argv[1:])
text = baseline.read_text()
assert "334ca4b7116d6b3ab636488d411716c9ef3850e5" in text
assert "checks: 48   failures: 0" in text and "RESULT: PASS" in text
assert "received stamped 490, unstamped 0, egress records lost 0" in text
print("baseline: PASS (48 checks in the separately completed baseline log)", flush=True)
print("head: " + subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip(), flush=True)
spec = importlib.util.spec_from_file_location("gptp_sw_mutants", repo / "tb/verilator/gptp_sw/gptp_sw_mutants.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert len(module.MUTANTS) == 14
failed = 0
with ThreadPoolExecutor(max_workers=8) as pool:
    pending = [pool.submit(module.one, work, mutant) for mutant in module.MUTANTS]
    for future in as_completed(pending):
        name, ok, words = future.result()
        failed += not ok
        print(f"{'ok' if ok else 'FAIL'} {name}: {words}", flush=True)
print(f"closed-loop plants: {len(module.MUTANTS)} checks, {failed} failures", flush=True)
print("RESULT: " + ("FAIL" if failed else "PASS"), flush=True)
sys.exit(bool(failed))
