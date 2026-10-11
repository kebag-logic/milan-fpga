"""Run the PR's own pin proof, census and pin controls from a checkout, in a given work directory.

Usage: python3 -B -I run_pin_controls.py <checkout> <workdir>
Prints the interpreter, the clean pin verdict, the census findings and every pin control line, then a summary.
"""
import sys
from pathlib import Path

checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
print("interpreter", sys.version.split()[0], flush=True)
import ctrl_build  # noqa: E402  (installs the proof's audit hook)
from ctrl_configs import makefiles  # noqa: E402
from ctrl_pin import pin_controls, proof_census  # noqa: E402

print("stack_pin", ctrl_build.stack_pin(), flush=True)
findings = proof_census()
print("census findings", len(findings), flush=True)
for f in findings:
    print("  CENSUS", f, flush=True)
work.mkdir(parents=True, exist_ok=True)
bad, total = pin_controls(work, makefiles())
print(f"SUMMARY interpreter={sys.version.split()[0]} pin_controls={total} misbehaved={bad} census={len(findings)}",
      flush=True)
sys.exit(1 if bad or findings else 0)
