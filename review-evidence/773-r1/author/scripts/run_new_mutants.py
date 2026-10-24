"""Run the clean dp control and the #773 planted controls of capture_coherence's
mutation arm, through the arm's own functions (mutants.py), in a temporary
directory. Run from the suite directory: python3 -I <this> <suite-dir> <jobs>."""
import sys, tempfile
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.path.insert(0, str(suite))
import mutants  # noqa: E402
with tempfile.TemporaryDirectory(prefix="a664-mutants-") as td:
    work = Path(td)
    made, lines = mutants.rom_images_result(work)
    if not made:
        print("\n".join(lines)); sys.exit(1)
    units = [u for u in mutants.arm_units(work)
             if u.name == "control/dp+dp-band" or (u.name.startswith("mutant/dp/") and "#773" in u.name)]
    print("units:", [u.name for u in units], flush=True)
    verdicts = mutants.run_units(units, jobs)
print(f"{len(verdicts)} checks: {sum(verdicts)} PASS, {len(verdicts) - sum(verdicts)} FAIL")
sys.exit(0 if all(verdicts) else 1)
