"""Run capture_coherence's dp positive control and the #773 planted controls
through the suite's own mutation driver (mutants.py), on N workers.
usage: python3 run_773_controls.py <capture_coherence dir> <jobs>"""
import os, sys, tempfile
from pathlib import Path
here = Path(sys.argv[1]).resolve()
os.chdir(here)
sys.path.insert(0, str(here))
import mutants  # the suite's own driver, at the reviewed head
with tempfile.TemporaryDirectory(prefix="r689-773-controls-") as td:
    made, lines = mutants.rom_images_result(Path(td))
    if not made:
        mutants.emit(lines)
        sys.exit(1)
    keep = [u for u in mutants.arm_units(Path(td), False)
            if u.name == "control/dp+dp-band" or (u.name.startswith("mutant/dp/") and "(#773)" in u.name)]
    print("[i] units:", [u.name for u in keep], flush=True)
    verdicts = mutants.run_units(keep, int(sys.argv[2]), None, Path(td))
print(f"\n{len(verdicts)} checks: {sum(verdicts)} PASS, {len(verdicts) - sum(verdicts)} FAIL", flush=True)
sys.exit(0 if all(verdicts) and verdicts else 1)
