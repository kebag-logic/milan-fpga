"""Round 2: plant one defect per run into an in-memory copy of a resmap module with the reviewer's
mutate_module.py (unchanged, sha256 recorded in the log) and require its self-test to go red; an
unmutated control must stay green. Prints one line per mutant and exits 0 only when every verdict is
the expected one."""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

LANE = Path("$LANES/652-builder-names")
TOOL = Path("/tmp/652-a533/r2/mutate_module.py")
SWEEP, MODELS, TABLES = "syn/resmap/yosys_sweep.py", "syn/resmap/resmap_models.py", "syn/resmap/resmap_tables.py"
MUTANTS = [
    ("r0 unmutated control", SWEEP, "failures += outcome != expected", "failures += outcome != expected", 0),
    ("r3 (R478-1) shapes ignores the expectation", SWEEP,
     "failures += outcome != expected", 'failures += outcome == "failed"', 1),
    ("r11 (R478-1) by_builder dropped", MODELS, 'result["guards"]["by_builder"] = builder', "pass", 1),
    ("shapes fails every step", SWEEP, "failures += outcome != expected", "failures += 1", 1),
    ("a refusal for another cause not counted", SWEEP, "        failures += foreign\\n", "", 1),
    ("the pinned cause ignored", SWEEP,
     'foreign = outcome == expected == "refused" and cause not in line', "foreign = False", 1),
    ("an expected refusal needs no cause", SWEEP,
     'if spec.get("expect") == "refused" and not (isinstance(cause, str) and cause):', "if False:", 1),
    ("a cause allowed on a built variant", SWEEP,
     'if spec.get("expect") != "refused" and cause is not None:', "if False:", 1),
    ("the plan accepts any expectation", SWEEP,
     'if spec.get("expect", "built") not in ("built", "refused"):', "if False:", 1),
    ("a traceback read as a refusal", SWEEP,
     ' and not any(line.startswith("Traceback") for line in lines)', "", 1),
    ("any exit with one refusal line read as a refusal", SWEEP,
     "if rc == 1 and len(refusals) == 1", "if len(refusals) == 1", 1),
    ("a variant with no outcome taken as built", SWEEP,
     "        raise PlanError(f\"{point['name']}: shape {shape} has no builder outcome; "
     "run the shapes command first\")", '        return ""', 1),
    ("run prices a builder-refused point", SWEEP,
     "        if line:\\n            print(f\"point {point['name']}: not priced",
     "        if False:\\n            print(f\"point {point['name']}: not priced", 1),
    ("summary accepts a priced receipt for a refused point", SWEEP,
     'if line and (directory / "receipt.json").is_file():', "if False:", 1),
    ("summary drops the builder record", SWEEP,
     '            summary[point["name"]] = {"builder": {"refusal": line}}\\n', "", 1),
    ("by_builder written with no builder-refused point", MODELS, "    if builder:\\n", "    if True:\\n", 1),
    ("a builder refusal not read as a refusal", MODELS,
     '    if builder is not None:\\n        return [builder["refusal"]]\\n', "", 1),
    ("an unpriced point given a marginal", MODELS,
     'name == reference or "hierarchical" not in summary.get(name, {}):',
     "name == reference or name not in summary:", 1),
    ("builder refusals labelled as guards", TABLES,
     '"builder" if name in builder else "elaboration guard"', '"elaboration guard"', 1),
]

print(f"tool {TOOL} sha256 {hashlib.sha256(TOOL.read_bytes()).hexdigest()}")
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=LANE, capture_output=True, text=True).stdout.strip()
print(f"head {head}")
wrong = 0
for label, module, old, new, want in MUTANTS:
    run = subprocess.run([sys.executable, str(TOOL), module, old, new], cwd=LANE, capture_output=True,
                         text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    rc = 1 if "SELFTEST rc=1" in run.stdout else 0 if "SELFTEST rc=0" in run.stdout else None
    first = next((line for line in (run.stdout + run.stderr).splitlines()
                  if "FAILED" in line or "raised" in line or "anchor" in line), "")
    verdict = "RED  " if rc == 1 else "GREEN" if rc == 0 else "ERROR"
    ok = rc == want
    wrong += not ok
    print(f"{'ok ' if ok else 'BAD'} {verdict} {Path(module).name}: {label} :: {first[:170]}")
print(f"{len(MUTANTS) - wrong}/{len(MUTANTS)} verdicts as expected "
      f"({sum(m[4] for m in MUTANTS)} mutants red required, 1 unmutated control green required)")
sys.exit(1 if wrong else 0)
