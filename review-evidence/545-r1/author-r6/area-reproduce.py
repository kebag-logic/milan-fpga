"""Reproduce the isolated area comparison without another checkout."""
from pathlib import Path
import os
import subprocess
import tempfile

root = Path.cwd()
base = "5c78ce2e9d831e588e759b696ed549804327e4d8"
with tempfile.TemporaryDirectory(prefix="milan-a320-area-") as directory:
    work = Path(directory)
    old_servo = work / "servo-dev.sv"
    old_servo.write_bytes(subprocess.check_output(
        ["git", "show", base + ":hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"], timeout=60))
    recipe = (root / "syn/yosys/ooc.sh").read_text()
    substitutions = {
        '. "$(dirname "$0")/malloc.sh"': '. "' + str(root / "syn/yosys/malloc.sh") + '"',
        'R="$(cd "$(dirname "$0")/../.." && pwd)"': 'R="' + str(root) + '"',
        '"KL_mmcm_drp_servo|$C/cdc_pulse.sv $C/cdc_handshake.sv $R/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"':
            '"KL_mmcm_drp_servo|$C/cdc_pulse.sv $C/cdc_handshake.sv ' + str(old_servo) + '"',
    }
    for before, after in substitutions.items():
        assert recipe.count(before) == 1, before
        recipe = recipe.replace(before, after, 1)
    base_recipe = work / "ooc-base.sh"
    base_recipe.write_text(recipe)
    for name, command in [
        ("current", [str(root / "syn/yosys/ooc.sh"), "KL_mmcm_drp_servo"]),
        ("base", ["bash", str(base_recipe), "KL_mmcm_drp_servo"]),
    ]:
        env = dict(os.environ, OOC_TMP=str(work / name))
        subprocess.run(["taskset", "-c", "10-15", *command], env=env,
                       check=True, timeout=21600)
